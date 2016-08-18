$(document).ready(function () {
    var currentDate = new Date();

    var dateTime = $("h1.datetime");
    var dateString = currentDate.toDateString();
    dateTime.text(dateString);

    // For responsive sidebar menu
    $("a.sidebar-toggle").click(function () {
        $('.ui.sidebar').sidebar('toggle');
    });

    switch (getPage()) {
        case "dashboard":
            setupDoughnut();
            break;
        case "products":
            setupProducts();
            break;
        case "sales":
            setupSalesLine();
            break;
        case "employees":
            setupNewEmployeeModal();
            setupCardDimmer();
            break;
        case "gallery":
            setupRatings();
            break;
        case "customers":
            setupAccordions();
            break;
    }

    function getPage() {
        return $("body").data("page");
    }

    function resizeGraphs() {
        if (getPage() === "sales") {
            var salesChart = $("#sales_chart");
            var table = $(".ui.table");
            salesChart.css("width", table.width());
        }
    }

    function setupDoughnut() {
        var ctx = document.getElementById("doughnuts_are_tasty").getContext("2d");
        var data = [
            {
                value: 300,
                color: "#F7464A",
                highlight: "#FF5A5E",
                label: "Red"
            },
            {
                value: 50,
                color: "#46BFBD",
                highlight: "#5AD3D1",
                label: "Green"
            },
            {
                value: 100,
                color: "#FDB45C",
                highlight: "#FFC870",
                label: "Yellow"
            }
        ]
        var myDoughnutChart = new Chart(ctx).Doughnut(data, {});

        var legendHolder = document.getElementById('dashboard_legend');
        legendHolder.innerHTML = myDoughnutChart.generateLegend();
    }

    function setupProducts() {
        $(".ui.selection.dropdown").dropdown();
        $(".ui.blue.import-export.buttons .ui.floating.dropdown").dropdown();
    }

    function setupSalesLine() {
        resizeGraphs();

        var ctx = document.getElementById("sales_chart").getContext("2d");
        var data = {
            labels: ["January", "February", "March", "April", "May", "June", "July"],
            datasets: [
                {
                    label: "My First dataset",
                    fillColor: "rgba(220,220,220,0.2)",
                    strokeColor: "rgba(220,220,220,1)",
                    pointColor: "rgba(220,220,220,1)",
                    pointStrokeColor: "#fff",
                    pointHighlightFill: "#fff",
                    pointHighlightStroke: "rgba(220,220,220,1)",
                    data: [65, 59, 80, 81, 56, 55, 40]
                },
                {
                    label: "My Second dataset",
                    fillColor: "rgba(151,187,205,0.2)",
                    strokeColor: "rgba(151,187,205,1)",
                    pointColor: "rgba(151,187,205,1)",
                    pointStrokeColor: "#fff",
                    pointHighlightFill: "#fff",
                    pointHighlightStroke: "rgba(151,187,205,1)",
                    data: [28, 48, 40, 19, 86, 27, 90]
                }
            ]
        };
        var myLineChart = new Chart(ctx).Line(data, {});
    }

    function setupNewEmployeeModal() {
        $("button.add-staff, .ui.inverted.icon.button, .ui.primary.icon.button, .ui.mobile.cards .ui.basic.green.button").on("click", function () {
            $(".ui.modal").modal("show");
        });
        $(".ui.checkbox").checkbox();
    }

    function setupCardDimmer() {
        $('.special.cards .image').dimmer({
            on: 'hover'
        });
    }

    function setupRatings() {
        $(".ui.star.rating").rating();
    }

    function setupAccordions() {
        $(".ui.accordion").accordion();
    }

    $(window).resize(function () {
        resizeGraphs()
    });
});