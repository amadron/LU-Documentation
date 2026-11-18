(() => {
  const SVG_NS = "http://www.w3.org/2000/svg";
  const CATEGORY_LABELS = {
    items: "Item sources",
    pets: "Pet placements",
  };

  function element(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text) node.textContent = text;
    return node;
  }

  function svgElement(tag, className) {
    const node = document.createElementNS(SVG_NS, tag);
    if (className) node.setAttribute("class", className);
    return node;
  }

  function markerDescription(marker) {
    return `${marker.name} (LOT ${marker.lot}) — XYZ ${marker.x}, ${marker.y}, ${marker.z}. ${marker.details}`;
  }

  function renderMap(container, data) {
    const imageUrl = new URL(container.dataset.mapImage, document.baseURI);
    const siteRoot = new URL(container.dataset.siteRoot, document.baseURI);
    const categoryFilter = container.dataset.category;
    const availableCategories = [...new Set(data.markers.map((marker) => marker.category))];
    const included = (marker) => categoryFilter === "all" || marker.category === categoryFilter;
    const baseMarkers = data.markers.filter(included);

    container.replaceChildren();
    const controls = element("div", "lu-location-map__controls");
    const search = element("input", "lu-location-map__search");
    search.type = "search";
    search.setAttribute("aria-label", "Filter map locations");
    search.placeholder = "Filter by name, LOT, or coordinates";
    controls.append(search);

    const categoryInputs = [];
    if (categoryFilter === "all" && availableCategories.length > 1) {
      const filters = element("fieldset", "lu-location-map__filters");
      const legend = element("legend", "", "Show on map");
      filters.append(legend);
      for (const category of availableCategories) {
        const label = element("label", "lu-location-map__filter");
        const checkbox = element("input");
        checkbox.type = "checkbox";
        checkbox.checked = true;
        checkbox.dataset.category = category;
        label.append(checkbox, document.createTextNode(` ${CATEGORY_LABELS[category] || category}`));
        filters.append(label);
        categoryInputs.push(checkbox);
      }
      controls.append(filters);
    }

    const count = element("p", "lu-location-map__count");
    const svg = svgElement("svg", "lu-location-map__svg");
    svg.setAttribute("viewBox", "0 0 1024 1024");
    svg.setAttribute("role", "img");
    svg.setAttribute("aria-label", `Zone ${data.zone} map with ${baseMarkers.length} static location markers`);
    const image = svgElement("image");
    image.setAttribute("href", imageUrl.href);
    image.setAttribute("width", "1024");
    image.setAttribute("height", "1024");
    image.setAttribute("preserveAspectRatio", "none");
    svg.append(image);

    const markerNodes = baseMarkers.map((marker) => {
      const link = svgElement("a", `lu-location-map__marker lu-location-map__marker--${marker.category}`);
      link.setAttribute("href", new URL(marker.path, siteRoot).href);
      link.setAttribute("tabindex", "0");
      link.setAttribute("aria-label", markerDescription(marker));
      link.dataset.search = `${marker.name} ${marker.lot} ${marker.x} ${marker.y} ${marker.z}`.toLocaleLowerCase();
      const highlight = svgElement("circle", "lu-location-map__marker-highlight");
      highlight.setAttribute("cx", marker.pixelX);
      highlight.setAttribute("cy", marker.pixelY);
      const circle = svgElement("circle");
      circle.setAttribute("cx", marker.pixelX);
      circle.setAttribute("cy", marker.pixelY);
      circle.setAttribute("r", "5");
      const title = svgElement("title");
      title.textContent = markerDescription(marker);
      link.append(highlight, circle, title);
      svg.append(link);
      return { marker, link };
    });

    let selectedMarker = null;
    const list = element("ul", "lu-location-map__list");
    const listNodes = markerNodes.map(({ marker, link }) => {
      const item = element("li", "lu-location-map__list-item");
      const select = element("button", "lu-location-map__select",
        `${marker.name} (LOT ${marker.lot})`);
      select.type = "button";
      select.setAttribute("aria-label", `Show ${marker.name} (LOT ${marker.lot}) on map`);
      select.setAttribute("aria-pressed", "false");
      select.addEventListener("click", () => {
        const deselecting = selectedMarker === marker;
        selectedMarker = deselecting ? null : marker;
        if (deselecting) {
          update();
          return;
        }
        svg.append(link);
        update();
        svg.scrollIntoView({ behavior: "smooth", block: "center" });
      });

      const source = element("a", "lu-location-map__source", "Details");
      source.href = new URL(marker.path, siteRoot).href;
      source.setAttribute("aria-label", `Open details for ${marker.name} (LOT ${marker.lot})`);
      const coordinates = element("span", "lu-location-map__coordinates",
        `XYZ ${marker.x}, ${marker.y}, ${marker.z}`);
      item.append(select, source, coordinates);
      list.append(item);
      return { marker, link, item, select };
    });

    const update = () => {
      const query = search.value.trim().toLocaleLowerCase();
      const checkedCategories = categoryInputs.length
        ? new Set(categoryInputs.filter((input) => input.checked).map((input) => input.dataset.category))
        : new Set(availableCategories);
      let shown = 0;
      for (const { marker, link, item, select } of listNodes) {
        const visible = marker.category !== undefined
          && checkedCategories.has(marker.category)
          && link.dataset.search.includes(query);
        link.classList.toggle("is-hidden", !visible);
        link.classList.toggle("is-selected", selectedMarker === marker);
        item.hidden = !visible;
        select.setAttribute("aria-pressed", String(selectedMarker === marker));
        if (visible) shown += 1;
      }
      count.textContent = `${shown} of ${baseMarkers.length} locations shown`;
    };

    search.addEventListener("input", update);
    categoryInputs.forEach((input) => input.addEventListener("change", update));
    container.append(
      controls,
      count,
      element("div", "lu-location-map__frame"),
    );
    container.querySelector(".lu-location-map__frame").append(svg);
    container.append(list);
    update();
  }

  async function initialise(container) {
    const response = await fetch(new URL(container.dataset.mapData, document.baseURI));
    if (!response.ok) {
      throw new Error(`map data request failed (${response.status})`);
    }
    const data = await response.json();
    renderMap(container, data);
  }

  document.querySelectorAll("[data-location-map]").forEach((container) => {
    initialise(container).catch((error) => {
      const message = element(
        "p",
        "lu-location-map__error",
        `Interactive map could not be loaded: ${error.message}. Use the XYZ coordinates in the tables.`,
      );
      container.replaceChildren(message);
      console.error("Failed to load location map", error);
    });
  });
})();
