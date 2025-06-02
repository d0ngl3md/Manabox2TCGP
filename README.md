# TCGPlayer Inventory Tool

This tool helps Magic: The Gathering sellers manage and price their inventory for upload to TCGPlayer. It allows you to compare your current inventory (from either ManaBox or a TCGPlayer export) with the latest TCGPlayer pricing data and export a CSV ready for upload.

## Features

- Supports two inventory formats:
  - **ManaBox** export (with `Quantity` and `Foil` columns)
  - **TCGPlayer** inventory export (with `Total Quantity` and `Condition`)
- Matches inventory with pricing data using:
  - Card Name
  - Set Name
  - Collector Number
  - Condition (`Near Mint` or `Near Mint Foil`)
- Applies a user-defined price floor
- Applies optional percentage markup
- Exports a valid TCGPlayer-format CSV:
  - Sets `Add to Quantity`
  - Updates `TCG Marketplace Price`

## Usage

1. **Launch the application.**
2. Select your **Inventory File** (CSV):
   - Choose between ManaBox or TCGPlayer format using the dropdown.
3. Select the **TCGPlayer Price File** (CSV) – typically downloaded from TCGPlayer pricing exports.
4. Choose:
   - Which price source to use: `TCG Low Price` or `TCG Market Price`
   - A **markup percentage** (optional)
   - A **price floor** (optional)
5. Click **Run** to generate the output.
6. Save the resulting CSV – it will be formatted for direct upload to TCGPlayer.

## Matching Logic

A row from your inventory is matched to the price sheet using:

- `Product Name` (or `Name` in ManaBox)
- `Set Name`
- `Collector Number`
- `Condition`:
  - ManaBox `"foil"` → `"Near Mint Foil"`
  - ManaBox `"normal"` → `"Near Mint"`
  - TCGPlayer uses `"Condition"` column directly (e.g. `"Near Mint"`)

Only cards with a **non-zero quantity** are included in the output.

## Output Rules

- The exported CSV retains all columns from the TCGPlayer price sheet.
- `Add to Quantity` is filled based on your inventory quantity:
  - From `Quantity` (ManaBox) or `Total Quantity` (TCGPlayer)
- `TCG Marketplace Price` is set as:
  - `max(price_source, floor) * (1 + markup%)`
- All prices are rounded to 2 decimal places.

## TODO / Future Enhancements

- [ ] Add checkbox to disable markup on price floor (apply markup only above floor)
- [ ] Allow condition selection (e.g., filter to `LP`, `NM`, etc.)
- [ ] Display warnings for unmatched rows
- [ ] Add support for other formats (e.g. Deckbox, Delver Lens)
- [ ] Generate price trend chart for each card
