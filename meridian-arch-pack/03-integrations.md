# 03-integrations

## Critical integration contract
**Boundary:** POS Client → Apollo Gateway  
**Purpose:** Look up a customer's active online cart at the POS after scanning the loyalty QR code.

## API style
**GraphQL over HTTPS**

## Operation
**Mutation / query name:** `cartLookupByLoyaltyQr`

## Authentication
- **Auth method:** Bearer token
- **Header:** `Authorization: Bearer <pos_access_token>`
- **Additional context header:** `X-Store-Id: <store_id>`
- POS token must represent an authenticated store-associate session with permission to view carts for assisted checkout.

## Request shape

```graphql
query cartLookupByLoyaltyQr($qrToken: String!, $storeId: ID!) {
  cartLookupByLoyaltyQr(qrToken: $qrToken, storeId: $storeId) {
    customerId
    cartId
    currency
    lineItems {
      sku
      name
      quantity
      price
      availabilityStatus
      availabilityConfidence
      lastConfirmedAt
    }
  }
}
```

### Request variables

```json
{
  "qrToken": "LOYALTY_QR_TOKEN",
  "storeId": "store-uk-042"
}
```

## Response shape

### Success response

```json
{
  "data": {
    "cartLookupByLoyaltyQr": {
      "customerId": "cust_12345",
      "cartId": "cart_98765",
      "currency": "EUR",
      "lineItems": [
        {
          "sku": "SKU-001",
          "name": "Cordless Drill Kit",
          "quantity": 1,
          "price": 129.99,
          "availabilityStatus": "LIKELY_AVAILABLE",
          "availabilityConfidence": 0.68,
          "lastConfirmedAt": "2026-06-08T10:42:00Z"
        }
      ]
    }
  }
}
```

## Error-code to user-state mapping

| Failure case | Gateway error code | Meaning | POS user state |
|---|---|---|---|
| Unknown loyalty ID / invalid QR token | `LOYALTY_ID_NOT_FOUND` | QR token cannot be resolved to a known customer | Show “Customer not found” and prompt associate to retry scan or search by another identifier |
| Cart not found | `CART_NOT_FOUND` | Customer exists but no active online cart is available | Show “No active online cart found” and allow associate to continue with a new in-store cart |
| Inventory-cache miss | `INVENTORY_STATUS_UNAVAILABLE` | Cart was found but availability could not be confirmed from the inventory cache | Show cart items with availability state “Stock unknown — confirm with floor staff”; do not block cart retrieval |
| Gateway timeout | `GATEWAY_TIMEOUT` | Downstream dependency exceeded timeout budget | Show retry action and a non-final fallback message; do not claim inventory certainty |
| Unauthorised POS session | `UNAUTHORISED` | Bearer token missing, expired, or lacks permission | Force re-authentication for the associate |

## Contract notes
- This integration must return the cart even when one line item has inventory uncertainty; availability uncertainty is a degraded state, not a hard failure for cart lookup.
- Availability data is **cache-first**. SAP ECC is not the default runtime dependency for every line item.
- If the inventory cache misses for one SKU, the response must preserve cart retrieval and map that line item to an explicit degraded user state instead of returning a generic error.
