function bar() {
  console.log("in bar");
  $.ajax({
    type: "POST",
    url: "/analytics_data",
  }).done(function (data) {
    data = String(data);
    let text = "[" + data + "]";
    data = JSON.parse(text);
    renderColumnChart(data);
    renderPieChart(data);
  });
}

function renderColumnChart(values) {
  var chart = new CanvasJS.Chart("columnChart", {
    backgroundColor: "#152b39",
    colorSet: "colorSet3",
    animationEnabled: true,
    legend: {
      verticalAlign: "bottom",
      horizontalAlign: "center",
    },
    theme: "theme2",
    data: [
      {
        indexLabelFontSize: 15,
        indexLabelFontFamily: "Monospace",
        indexLabelFontColor: "darkgrey",
        indexLabelLineColor: "darkgrey",
        indexLabelPlacement: "outside",
        type: "column",
        showInLegend: false,
        legendMarkerColor: "grey",
        dataPoints: values,
      },
    ],
  });

  chart.render();
}

function renderPieChart(values) {
  var chart = new CanvasJS.Chart("pieChart", {
    backgroundColor: "#152b39",
    colorSet: "colorSet2",
    animationEnabled: true,
    data: [
      {
        indexLabelFontSize: 15,
        indexLabelFontFamily: "Monospace",
        indexLabelFontColor: "darkgrey",
        indexLabelLineColor: "darkgrey",
        indexLabelPlacement: "outside",
        type: "pie",
        showInLegend: false,
        toolTipContent: "<strong>#percent%</strong>",
        dataPoints: values,
      },
    ],
  });
  chart.render();
}
