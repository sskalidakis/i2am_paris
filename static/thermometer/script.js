
const units = {
  Celcius: "°C",
  Fahrenheit: "°F" };


const config = {
  minTemp: -20,
  maxTemp: 50,
  unit: "Celcius" };


// Change min and max temperature values

const tempValueInputs = document.querySelectorAll("input[type='text']");

tempValueInputs.forEach(input => {
  input.addEventListener("change", event => {
    const newValue = event.target.value;

    if (isNaN(newValue)) {
      return input.value = config[input.id];
    } else {
      config[input.id] = input.value;
      range[input.id.slice(0, 3)] = config[input.id]; // Update range
      return setTemperature(); // Update temperature
    }
  });
});

// Switch unit of temperature

const unitP = document.getElementById("unit");

unitP.addEventListener("click", () => {
  config.unit = config.unit === "Celcius" ? "Fahrenheit" : "Celcius";
  unitP.innerHTML = config.unit + ' ' + units[config.unit];
  return setTemperature();
});

// Change temperature

const range = document.querySelector("input[type='range']");
const temperature = document.getElementById("temperature");

function setTemperature() {
  temperature.style.height = (range.value - config.minTemp) / (config.maxTemp - config.minTemp) * 100 + "%";
  temperature.dataset.value = range.value + units[config.unit];
}


// function lineChart(t) {
var t= 1;
  am4core.ready(function() {

// Themes begin
    am4core.useTheme(am4themes_animated);
// Themes end

// Create chart instance
    var chart = am4core.create("chartdiv", am4charts.XYChart);

// Add data
//    chart.data = myData(1);
// TODO do it with record
    chart.data = [];

// Set input format for the dates
    chart.dateFormatter.inputDateFormat = "yyyy-MM-dd";

// Create axes
    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());

// Create series
    var series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.valueY = "value";
    series.dataFields.dateX = "date";
    series.tooltipText = "{value}"
    series.strokeWidth = 2;
    series.minBulletDistance = 15;

// Drop-shaped tooltips
    series.tooltip.background.cornerRadius = 20;
    series.tooltip.background.strokeOpacity = 0;
    series.tooltip.pointerOrientation = "vertical";
    series.tooltip.label.minWidth = 40;
    series.tooltip.label.minHeight = 40;
    series.tooltip.label.textAlign = "middle";
    series.tooltip.label.textValign = "middle";

// Make bullets grow on hover
    var bullet = series.bullets.push(new am4charts.CircleBullet());
    bullet.circle.strokeWidth = 2;
    bullet.circle.radius = 4;
    bullet.circle.fill = am4core.color("#fff");

    var bullethover = bullet.states.create("hover");
    bullethover.properties.scale = 1.3;

// Make a panning cursor
    chart.cursor = new am4charts.XYCursor();
    chart.cursor.behavior = "panXY";
    chart.cursor.xAxis = dateAxis;
    chart.cursor.snapToSeries = series;

// Create vertical scrollbar and place it before the value axis
    chart.scrollbarY = new am4core.Scrollbar();
    chart.scrollbarY.parent = chart.leftAxesContainer;
    chart.scrollbarY.toBack();

// Create a horizontal scrollbar with previe and place it underneath the date axis
    chart.scrollbarX = new am4charts.XYChartScrollbar();
    chart.scrollbarX.series.push(series);
    chart.scrollbarX.parent = chart.bottomAxesContainer;

    dateAxis.start = 0.79;
    dateAxis.keepSelection = true;




// }


document.getElementById("termometer").addEventListener("wheel", myFunction);
var temp = 0;
function myFunction(e) {
  if (e.deltaY < 0) {
    if (config.maxTemp > temp) {
      temp += 1;}
  } else {
    if (config.minTemp < temp) {
      temp -= 1;
    }

  }

//  chart.data= myData(temp);
// TODO in case of recorddata
  chart.data= recordDataFun(temp);
  temperature.style.height = (temp - config.minTemp) / (config.maxTemp - config.minTemp) * 100 + "%";
  temperature.dataset.value = temp + units[config.unit];
}
// var flag= true;
// if (flag) {
//   lineChart(1);
//   flag = false;
// }
  }); // end am4core.ready()
function myData(t) {
  tempInputData = inputData;
  for (let i = 0; i < tempInputData.length; i++){
            tempInputData[i].value = tempInputData[i].value *t;
            }
  return tempInputData;

}


function recordDataFun(key){
// In case we have records
if (recordData[key]=== undefined){
    // If there isn't this key return empty array
    return [];
}else{
        return recordData[key];
}
}