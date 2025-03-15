async function loadConfig() {
    const response = await fetch("api/config/");
    const data = await response.json();
    window.APP_BASE_URL = data.APP_BASE_URL;
    localStorage.setItem("APP_BASE_URL", data.APP_BASE_URL);
    console.log("APP_BASE_URL:", window.APP_BASE_URL);
}


$(document).ready(function () {
    if (localStorage.getItem("APP_BASE_URL")) {
        window.APP_BASE_URL = localStorage.getItem("APP_BASE_URL");
    }
    else {
        loadConfig();
    }
    let typingTimer;
    const typingDelay = 800; // 0.8s delay

    $("#nse_codes").on("input", function () {
        clearTimeout(typingTimer);
        let query = $(this).val().trim();
        console.log(query.length);
        if (query.length < 3) {
            $("#error-msg").show();
            $("#dropdown").hide(); // Hide dropdown if input is invalid
        } else {
            $("#error-msg").hide();

            //API call only when length is 3 or more
            typingTimer = setTimeout(() => {
                if (query.length >= 3 && APP_BASE_URL) {
                    fetchMatchingKeywords(query);
                }
            }, typingDelay);
        }
    });

    function fetchMatchingKeywords(query) {
        $.ajax({
            url: `${APP_BASE_URL}/fetch_nse/?q=${query}`, // API call
            method: "GET",
            success: function (data) {
                displayDropdown(data.symbols);
            },
            error: function (e) {
                console.log("error is", e);
                console.log("error is", e?.responseJSON?.detail);
                let errorMessage = e?.responseJSON?.detail || "Error fetching stock details.";

                // Ensure error is displayed in the correct section
                $("#result").html(`<p class="error-message">${errorMessage}</p>`);
            }
        });
    }

    function displayDropdown(symbols) {
        let dropdownHtml = "";

        if (symbols.length === 0) {
            dropdownHtml = '<p class="no-result">No results found</p>';
        } else {
            symbols.forEach(item => {
                dropdownHtml += `<div class="dropdown-item" data-symbol="${item.symbol}">
                                    <strong>${item.symbol}</strong> - ${item.symbol_info}
                                </div>`;
            });
        }

        $("#dropdown").html(dropdownHtml).show();
    }

    // Handle selection from dropdown
    $(document).on("click", ".dropdown-item", function () {
        let selectedSymbol = $(this).data("symbol");
        $("#nse_codes").val(selectedSymbol);
        $("#dropdown").hide();
    });

    // Hide dropdown when clicking outside
    $(document).click(function (event) {
        if (!$(event.target).closest(".autocomplete-wrapper").length) {
            $("#dropdown").hide();
        }
    });

    $("#submit_btn").on("click", function () {
        let selectedSymbol = $("#nse_codes").val().trim();

        if (selectedSymbol.length < 3) {
            alert("Please enter at least 3 characters.");
        } else {
            fetchStockDetails(selectedSymbol);
        }
    });

    function fetchStockDetails(symbol) {
        $.ajax({
            url: `${APP_BASE_URL}/diff-ath-cmp?codes=${symbol}`,
            method: "GET",
            success: function (data) {
                displayStockDetails(data);
            },
            error: function (e) {
                console.log("erro is", e);
                console.log("error is", e?.responseJSON?.detail);
                let errorMessage = e?.responseJSON?.detail || "Error fetching stock details.";

                // Ensure error is displayed in the correct section
                $("#result").html(`<p class="error-message">${errorMessage}</p>`);
            }
        });
    }

    function displayStockDetails(data) {
        let resultHtml = `
            <h3>Stock Details for: ${data.stock_name}</h3>
            <p><strong>ATH:</strong> ${data.all_time_high}</p>
            <p><strong>Current Price:</strong> ${data.current_price}</p>
            <p><strong>Difference:</strong> ${data.percentage_difference}</p>
        `;

        $("#result").html(resultHtml);
    }
});
