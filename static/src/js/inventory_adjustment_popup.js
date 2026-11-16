/** @odoo-module */
import { Component, proxy } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class InventoryAdjustmentPopup extends Component {
  static template = "pos_hide_closing_register.InventoryAdjustmentPopup";
  static components = { Dialog };

  setup() {
    // OWL 3 in Odoo 20 uses proxy() instead of useState()
    this.state = proxy({
      lines: [],
      selectedProductId: "",
      searchQuery: "",
      inputQty: "",
      dropdownOpen: false,
    });
  }

  get selectedProduct() {
    if (!this.state.selectedProductId) return null;
    return (this.props.products || []).find(
      (p) => p.id === parseInt(this.state.selectedProductId, 10),
    );
  }

  get availableProducts() {
    const addedIds = this.state.lines.map((l) => l.product_id);
    const query = (this.state.searchQuery || "").trim().toLowerCase();
    return (this.props.products || []).filter((p) => {
      if (addedIds.includes(p.id)) return false;
      if (!query) return true;
      return (p.display_name || "").toLowerCase().includes(query);
    });
  }

  getImageUrl(productId) {
    return `/web/image?model=product.product&field=image_128&id=${productId}`;
  }

  toggleDropdown() {
    this.state.dropdownOpen = !this.state.dropdownOpen;
  }

  selectProduct(productId) {
    this.state.selectedProductId = productId;
    this.state.dropdownOpen = false;
    this.state.searchQuery = "";
  }

  onKeypadClick(value) {
    if (value === "C") {
      this.state.inputQty = "";
    } else if (value === "BACK") {
      this.state.inputQty = this.state.inputQty.slice(0, -1);
    } else if (value === ".") {
      if (!this.state.inputQty.includes(".")) {
        this.state.inputQty = (this.state.inputQty || "0") + ".";
      }
    } else {
      if (this.state.inputQty === "0") {
        this.state.inputQty = value;
      } else {
        this.state.inputQty += value;
      }
    }
  }

  addLine() {
    const productId = parseInt(this.state.selectedProductId, 10);
    const qty = parseFloat(this.state.inputQty);

    if (!productId || isNaN(qty)) {
      return;
    }

    const product = (this.props.products || []).find((p) => p.id === productId);
    if (!product) return;

    if (this.state.lines.some((l) => l.product_id === productId)) {
      return;
    }

    this.state.lines.push({
      id: Date.now(),
      product_id: productId,
      product_name: product.display_name,
      quantity: qty,
    });

    this.state.selectedProductId = "";
    this.state.inputQty = "";
  }

  removeLine(id) {
    this.state.lines = this.state.lines.filter((l) => l.id !== id);
  }

  confirm() {
    // If user selected a product and typed a quantity but forgot to press '+', add it automatically
    if (this.state.selectedProductId && this.state.inputQty !== "") {
      this.addLine();
    }
    this.props.getPayload(this.state.lines);
    this.props.close();
  }

  cancel() {
    this.props.close();
  }
}
