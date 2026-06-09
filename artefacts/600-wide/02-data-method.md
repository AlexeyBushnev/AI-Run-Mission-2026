# 02-data-method

- Tool used: AI-assisted synthetic data generation in chat, then manual review.
- Source fields covered: `customer_id`, `order_id`, `store_id`, `payment_method`, `loyalty_number`.
- Records created: 5 realistic + 10 edge-case records.
- Obfuscation method: all values are fully fictional replacements; no production names, emails, phone numbers, addresses, or live payment details were used.
- Shape preserved: region prefixes, loyalty formats, and payment-method patterns were kept plausible so end-to-end flows still look realistic.
- Variety dimensions exercised: country/market band (Italy, Germany, Japan, UK, US), payment method, cross-region pickup, identity-merge state, malformed input, expiry state, length boundary, and multilingual script.
- Special-character coverage includes accents, ß, Japanese kana, and Arabic script.
- PSD2-relevant methods included: Postepay, Satispay, Klarna split-pay style, Visa/Mastercard.
- Intentionally missing: regions not yet onboarded to Phase 1, real customer PII, and full item-level basket payloads beyond the order-level markers.
- Re-run recipe: regenerate the same 5 realistic + 10 edge records with the same field list and preserve the same variety dimensions and fictional-only rule.
