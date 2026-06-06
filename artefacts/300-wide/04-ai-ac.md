# 04-ai-ac

## User story

As a click-&-collect shopper, I want to see estimated store availability with a visible confidence cue before I reserve, so that I can avoid a wasted trip when stock is uncertain.

## Base AC

**AC1.** When a product has store stock data, then the product page shows an availability indicator per nearby store.
**AC2.** When no store within range has the item, then show “Not collectable nearby” and a delivery option.
**AC3.** When stock data is missing for a store, then omit that store and do not guess.
**AC4.** When the user taps a store, then show last-confirmed time and distance.

## AI-specific AC

**AI-AC1 (confidence)**
When stock confidence for a store is below **0.70**, the label must not say **“In stock”**; it must show a lower-confidence label such as **“Likely available”**.

**AI-AC2 (refusal / fallback)**
When stock data is older than **30 minutes** or confidence cannot be calculated, the assistant must not estimate collectability and must show **“Check with store”** plus the store contact option.

**AI-AC3 (latency)**
For **95%** of product-page loads, availability results for nearby stores must render within **2 seconds** after the page becomes interactive.

**AI-AC4 (disclosure)**
Every estimated availability result must display that it is an **estimate from store data**, not a guaranteed hold, in visible product-page text or an adjacent explainer.

**AI-AC5 (feedback)**
When a shopper sees a low-confidence or fallback result, the interface must provide a visible feedback action, and feedback submission success must be confirmed in the UI.

**AI-AC6 (negative AC)**
The assistant must **not** state an exact shelf quantity and must **not** imply that the item is reserved, held, or guaranteed for pickup unless a separate hold-confirmation flow has completed.
