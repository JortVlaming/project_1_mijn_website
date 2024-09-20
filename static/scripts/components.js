class CustomSearchBar extends HTMLElement {
    constructor() {
        super();
    }

    connectedCallback() {
        this.innerHTML = "" +
            "<form action=\"search\" id=\"search\">" +
            "   <input type=\"text\" placeholder=\"Student naam\" id=\"query\" name=\"query\">\n" +
            "   <button type=\"submit\">Search</button>\n" +
            "</form>";
    }
}

customElements.define('custom-search-bar', CustomSearchBar);
