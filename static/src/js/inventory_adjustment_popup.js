/** @odoo-module */
import { Component, proxy, signal, useProps } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class InventoryAdjustmentPopup extends Component {
  static template = "pos_hide_closing_register.InventoryAdjustmentPopup";
  static components = { Dialog };

  props = useProps();

  // OWL 3 t-model requires signal() primitives
  searchQuery = signal("");
  inputQty = signal("");

  setup() {
    this.state = proxy({
      lines: [],
      selectedProductId: "",
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
    const query = (this.searchQuery() || "").trim().toLowerCase();
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
    this.searchQuery.set("");
  }

  onKeypadClick(value) {
    const current = this.inputQty() || "";
    if (value === "C") {
      this.inputQty.set("");
    } else if (value === "BACK") {
      this.inputQty.set(current.slice(0, -1));
    } else if (value === ".") {
      if (!current.includes(".")) {
        this.inputQty.set((current || "0") + ".");
      }
    } else {
      if (current === "0") {
        this.inputQty.set(value);
      } else {
        this.inputQty.set(current + value);
      }
    }
  }

  addLine() {
    const productId = parseInt(this.state.selectedProductId, 10);
    const qty = parseFloat(this.inputQty());

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
    this.inputQty.set("");
  }

  removeLine(id) {
    this.state.lines = this.state.lines.filter((l) => l.id !== id);
  }

  confirm() {
    // If user selected a product and typed a quantity but forgot to press '+', add it automatically
    if (this.state.selectedProductId && this.inputQty() !== "") {
      this.addLine();
    }
    this.props.getPayload(this.state.lines);
    this.props.close();
  }

  cancel() {
    this.props.close();
  }
}
