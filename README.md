# POS Hide Closing Register & Custom Sales Details (Odoo 20)

This **Odoo 20** module streamlines the Point of Sale (POS) session closing process by replacing the standard Closing Control popup with an automated workflow, an integrated **Closing Inventory Check**, and a customizable **Custom Sales Details** thermal report.

---

## Features

### 1. Automated Register Closing
- **One-Click Session Closure**: Skips the standard "Closing Control" popup when enabled.
- **Automatic Cash Reconciliation**: Retrieves expected cash balances, posts closing cash details, updates closing control state, and closes the session cleanly.
- **Session Cleanup**: Automatically clears browser storage for the closed session and returns to the POS start screen.

### 2. Closing Inventory Check Popup
- **Pre-Closing Stock Count**: Prompts the cashier to record physical inventory counts before the register closes.
- **Product Filtering & Search**:
  - Restrict the list to specific products configured on the POS terminal, or allow counting any POS product.
  - Includes a built-in search bar inside the product selector dropdown.
- **Touchscreen Numpad**: Built-in on-screen keypad for entering quantities quickly.
- **Automatic Stock Adjustment & Audit Log**:
  - Updates `stock.quant` quantities in the POS source location automatically.
  - Saves a log of **Previous Stock**, **Counted Stock**, and **Difference** on the `pos.session` record for reporting.

### 3. Custom Sales Details Report
- **Auto-Print on Close & Backend Reprint**: Automatically prints upon session closure (via **Chrome Print Preview** or **QZ Tray** direct thermal printing) and can be reprinted anytime from the backend **POS Session → Print → Custom Sales Details** menu.
- **Customizable Branding & Labels**:
  - Custom **Report Title** (e.g., `SESSION REPORT`)
  - Custom **Header Note / Subtitle**
  - Custom **Footer Message**
  - Configurable **Currency Label** (defaults to `DH`)
- **Granular Section Toggles**: Enable or disable any section per POS terminal:
  1. **Company Info**: Company name, address, and phone number.
  2. **Session & Order Summary**: POS terminal name, Session ID, Cashier, timezone-adjusted Opened/Closed timestamps, total order count, and total items sold.
  3. **Cash Register Balances**: Opening Cash, Expected Cash, Counted Cash, and Difference.
  4. **Sales Breakdown by Category & Product**: Groups items by their primary POS Category (including **Uncategorized** items, with no multi-category double counting).
  5. **Taxes, Discounts & Refunds**: Net Sales (Excl. Tax), Total Taxes, Total Discounts, and Refunds count/amount.
  6. **Payment Methods Breakdown**: Totals collected per payment method.
  7. **Closing Inventory Counts**: Prints the exact inventory counts and stock differences recorded by the cashier during closing.

---

## Configuration

1. Navigate to **Point of Sale → Configuration → Point of Sale** and open your POS terminal.
2. In the **Closing & Inventory Check** section:
   - Enable **Hide Closing Register Popup**.
   - Enable **Enable Closing Inventory Check** and optionally select specific products in **Inventory Adjustment Products**.
   - Enable **Auto-Print Sales Details on Close** and choose your **Print Method** (*Chrome Print Preview* or *QZ Tray*).
3. In the **Custom Sales Details Report** section:
   - Customize the **Report Title**, **Custom Header Note**, **Custom Footer Message**, and **Currency Label**.
   - Check or uncheck the **Visible Report Sections** according to your store's requirements.

---

## Usage

1. Open a POS session and process orders as usual.
2. Click **Close Register** in the POS menu.
3. **Closing Inventory Check** *(if enabled)*:
   - Select each product to count, enter the quantity using the keypad, and click **`+`**.
   - Click **Validate & Close** to apply stock adjustments and proceed, or **Cancel** to return to the session.
4. The session closes automatically and prints the **Custom Sales Details** report.

---

## Technical Details

- **Odoo Version**: `20.0.2.0.0`
- **Module Name**: `pos_hide_closing_register`
- **Dependencies**: `point_of_sale`, `stock`
- **Odoo 20 Architecture**:
  - **OWL 3 Frontend**: Uses `proxy()` reactive state, mandatory `this.` template bindings, and `t-out` directives.
  - **Material Symbols Icons**: Uses Odoo 20's Material Symbols ligature icons (`delete`, `arrow_drop_down`, `add`).
  - **Timezone Handling**: Uses Python's `zoneinfo.ZoneInfo` (`self.env.tz`) for accurate local timestamps on thermal reports.

---

## Installation

1. Copy the `pos_hide_closing_register` folder into your Odoo 20 `addons` directory.
2. Restart the Odoo server.
3. Enable **Developer Mode** and go to **Apps → Update Apps List**.
4. Search for **POS Hide Closing Register & Custom Sales Details** and click **Activate**.

---

## License

LGPL-3