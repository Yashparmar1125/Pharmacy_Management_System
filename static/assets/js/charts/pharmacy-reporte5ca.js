"use strict";
!function(NioApp, $) {
    // Define NioApp
    NioApp = {
        State: {
            isRTL: false
        },
        coms: {
            docReady: []
        },
        hexRGB: function(hex, alpha) {
            var r = parseInt(hex.slice(1, 3), 16);
            var g = parseInt(hex.slice(3, 5), 16);
            var b = parseInt(hex.slice(5, 7), 16);
            return `rgba(${r}, ${g}, ${b}, ${alpha})`;
        }
    };

    var toDay = {
            labels: ["12AM - 02AM", "02AM - 04AM", "04AM - 06AM", "06AM - 08AM", "08AM - 10AM", "10AM - 12PM", "12PM - 02PM", "02PM - 04PM", "04PM - 06PM", "06PM - 08PM", "08PM - 10PM", "10PM - 12PM"],
            dataUnit: "USD",
            lineTension: .3,
            datasets: [{
                label: "USD",
                color: "#0fac81",
                background: "transparent",
                data: [920, 1005, 1250, 850, 1100, 1006, 1310, 1050, 1100, 1310, 1050, 1100]
            }]
        },
        thisWeek = {
            labels: ["12AM - 02AM", "02AM - 04AM", "04AM - 06AM", "06AM - 08AM", "08AM - 10AM", "10AM - 12PM", "12PM - 02PM", "02PM - 04PM", "04PM - 06PM", "06PM - 08PM", "08PM - 10PM", "10PM - 12PM"],
            dataUnit: "USD",
            lineTension: .3,
            datasets: [{
                label: "USD",
                color: "#816bff",
                background: "transparent",
                data: [920, 1050, 1250, 850, 1100, 1006, 1310, 1050, 1100, 1310, 1050, 1100]
            }]
        },
        thisMonth = {
            labels: ["12AM - 02AM", "02AM - 04AM", "04AM - 06AM", "06AM - 08AM", "08AM - 10AM", "10AM - 12PM", "12PM - 02PM", "02PM - 04PM", "04PM - 06PM", "06PM - 08PM", "08PM - 10PM", "10PM - 12PM"],
            dataUnit: "USD",
            lineTension: .3,
            datasets: [{
                label: "USD",
                color: "#2c3782",
                background: "transparent",
                data: [920, 1050, 1250, 850, 1100, 1060, 1310, 1050, 1100, 1310, 1050, 1100]
            }]
        },
        thisYear = {
            labels: ["12AM - 02AM", "02AM - 04AM", "04AM - 06AM", "06AM - 08AM", "08AM - 10AM", "10AM - 12PM", "12PM - 02PM", "02PM - 04PM", "04PM - 06PM", "06PM - 08PM", "08PM - 10PM", "10PM - 12PM"],
            dataUnit: "USD",
            lineTension: .3,
            datasets: [{
                label: "USD",
                color: "#1c2b46",
                background: "transparent",
                data: [920, 1050, 1250, 850, 1100, 1060, 1310, 1050, 1100, 1310, 1050, 1100]
            }]
        },
        electricity = {
            labels: ["12AM - 02AM", "02AM - 04AM", "04AM - 06AM", "06AM - 08AM", "08AM - 10AM", "10AM - 12PM", "12PM - 02PM", "02PM - 04PM", "04PM - 06PM", "06PM - 08PM", "08PM - 10PM", "10PM - 12PM"],
            dataUnit: "USD",
            lineTension: .3,
            datasets: [{
                label: "USD",
                color: "#e85347",
                background: "transparent",
                data: [920, 1005, 1250, 850, 1100, 1006, 1310, 1050, 1100, 1310, 1050, 1100]
            }]
        },
        equipements = {
            labels: ["12AM - 02AM", "02AM - 04AM", "04AM - 06AM", "06AM - 08AM", "08AM - 10AM", "10AM - 12PM", "12PM - 02PM", "02PM - 04PM", "04PM - 06PM", "06PM - 08PM", "08PM - 10PM", "10PM - 12PM"],
            dataUnit: "USD",
            lineTension: .3,
            datasets: [{
                label: "USD",
                color: "#f4bd0e",
                background: "transparent",
                data: [920, 1050, 1250, 850, 1100, 1006, 1310, 1050, 1100, 1310, 1050, 1100]
            }]
        },
        maintenance = {
            labels: ["12AM - 02AM", "02AM - 04AM", "04AM - 06AM", "06AM - 08AM", "08AM - 10AM", "10AM - 12PM", "12PM - 02PM", "02PM - 04PM", "04PM - 06PM", "06PM - 08PM", "08PM - 10PM", "10PM - 12PM"],
            dataUnit: "USD",
            lineTension: .3,
            datasets: [{
                label: "USD",
                color: "#2c3782",
                background: "transparent",
                data: [920, 1050, 1250, 850, 1100, 1060, 1310, 1050, 1100, 1310, 1050, 1100]
            }]
        },
        rents = {
            labels: ["12AM - 02AM", "02AM - 04AM", "04AM - 06AM", "06AM - 08AM", "08AM - 10AM", "10AM - 12PM", "12PM - 02PM", "02PM - 04PM", "04PM - 06PM", "06PM - 08PM", "08PM - 10PM", "10PM - 12PM"],
            dataUnit: "USD",
            lineTension: .3,
            datasets: [{
                label: "USD",
                color: "#1c2b46",
                background: "transparent",
                data: [920, 1050, 1250, 850, 1100, 1060, 1310, 1050, 1100, 1310, 1050, 1100]
            }]
        };

    function ecommerceLineS3(selector, set_data) {
        var $selector = $(selector || ".ecommerce-line-chart-s3");
        $selector.each(function() {
            for (var $self = $(this), _self_id = $self.attr("id"), _get_data = void 0 === set_data ? eval(_self_id) : set_data, selectCanvas = document.getElementById(_self_id).getContext("2d"), chart_data = [], i = 0; i < _get_data.datasets.length; i++) chart_data.push({
                label: _get_data.datasets[i].label,
                tension: _get_data.lineTension,
                backgroundColor: _get_data.datasets[i].background,
                fill: !0,
                borderWidth: 2,
                borderColor: _get_data.datasets[i].color,
                pointBorderColor: "transparent",
                pointBackgroundColor: "transparent",
                pointHoverBackgroundColor: "#fff",
                pointHoverBorderColor: _get_data.datasets[i].color,
                pointBorderWidth: 2,
                pointHoverRadius: 4,
                pointHoverBorderWidth: 2,
                pointRadius: 4,
                pointHitRadius: 4,
                data: _get_data.datasets[i].data
            });
            var chart = new Chart(selectCanvas, {
                type: "line",
                data: {
                    labels: _get_data.labels,
                    datasets: chart_data
                },
                options: {
                    plugins: {
                        legend: {
                            display: _get_data.datasets.length > 1,
                            labels: {
                                color: "#a8a8a8"
                            }
                        },
                        tooltip: {
                            mode: "index",
                            intersect: !1,
                            callbacks: {
                                label: function(tooltipItem) {
                                    return tooltipItem.dataset.label + ": " + tooltipItem.parsed.y + " " + _get_data.dataUnit;
                                }
                            }
                        }
                    },
                    responsive: !0,
                    maintainAspectRatio: !1,
                    scales: {
                        y: {
                            ticks: {
                                color: "#a8a8a8",
                                beginAtZero: !0
                            }
                        },
                        x: {
                            ticks: {
                                color: "#a8a8a8"
                            }
                        }
                    }
                }
            });
        });
    }

    NioApp.coms.docReady.push(function() {
        ecommerceLineS3();
    });

    var totalSales = {
            labels: ["January", "February", "March", "April", "May", "June", "July"],
            datasets: [{
                label: "Sales",
                backgroundColor: "#0fac81",
                borderColor: "#0fac81",
                borderWidth: 1,
                data: [40, 39, 10, 40, 39, 80, 40]
            }]
        },
        totalOrders = {
            labels: ["January", "February", "March", "April", "May", "June", "July"],
            datasets: [{
                label: "Orders",
                backgroundColor: "#816bff",
                borderColor: "#816bff",
                borderWidth: 1,
                data: [50, 70, 20, 90, 80, 50, 60]
            }]
        },
        totalCustomers = {
            labels: ["January", "February", "March", "April", "May", "June", "July"],
            datasets: [{
                label: "Customers",
                backgroundColor: "#f4bd0e",
                borderColor: "#f4bd0e",
                borderWidth: 1,
                data: [90, 80, 60, 70, 60, 80, 90]
            }]
        };

    function ecommerceLineS1(selector, set_data) {
        var $selector = $(selector || ".ecommerce-line-chart-s1");
        $selector.each(function() {
            for (var $self = $(this), _self_id = $self.attr("id"), _get_data = void 0 === set_data ? eval(_self_id) : set_data, selectCanvas = document.getElementById(_self_id).getContext("2d"), chart_data = [], i = 0; i < _get_data.datasets.length; i++) chart_data.push({
                label: _get_data.datasets[i].label,
                backgroundColor: _get_data.datasets[i].backgroundColor,
                borderColor: _get_data.datasets[i].borderColor,
                borderWidth: _get_data.datasets[i].borderWidth,
                data: _get_data.datasets[i].data
            });
            var chart = new Chart(selectCanvas, {
                type: "line",
                data: {
                    labels: _get_data.labels,
                    datasets: chart_data
                },
                options: {
                    plugins: {
                        legend: {
                            display: !1
                        },
                        tooltip: {
                            mode: "index",
                            intersect: !1,
                            callbacks: {
                                label: function(tooltipItem) {
                                    return tooltipItem.dataset.label + ": " + tooltipItem.parsed.y;
                                }
                            }
                        }
                    },
                    responsive: !0,
                    maintainAspectRatio: !1,
                    scales: {
                        y: {
                            ticks: {
                                color: "#a8a8a8",
                                beginAtZero: !0
                            }
                        },
                        x: {
                            ticks: {
                                color: "#a8a8a8"
                            }
                        }
                    }
                }
            });
        });
    }

    NioApp.coms.docReady.push(function() {
        ecommerceLineS1();
    });

}(window.NioApp = window.NioApp || {}, jQuery);
