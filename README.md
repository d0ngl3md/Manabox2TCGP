# TCGPlayer Inventory Tool

A desktop application written in Python using `tkinter` and `ttkbootstrap` that helps Magic: The Gathering sellers synchronize their inventory data with TCGPlayer pricing sheets. It supports both [ManaBox](https://manabox.app) exports and TCGPlayer inventory exports and allows users to update pricing fields and quantities for easy CSV upload.

## Features

- ✅ Supports **ManaBox** and **TCGPlayer** inventory formats.
- ✅ Accepts TCGPlayer **pricing CSV exports** as a price reference.
- ✅ Automatically **matches cards** based on:
  - Card Name
  - Set Name
  - Collector Number
  - Card Condition (e.g., Near Mint, Near Mint Foil)
- ✅ Applies:
  - **Price floor**
  - **Markup percentage**
- ✅ Outputs an updated TCGPlayer-compatible CSV:
  - Updates `Add to Quantity` with your inventory values
  - Updates `TCG Marketplace Price` with adjusted prices
- ✅ Themeable GUI using `ttkbootstrap` (Vapor theme by default)

## Requirements

- Python 3.7+
- `pandas`
- `ttkbootstrap`

Install dependencies:

```bash
pip install pandas ttkbootstrap
