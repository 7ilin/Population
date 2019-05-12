window.chart = null;

window.onload = function() {
    loadRegion();
    setHandlers();
}

function loadRegion() {
    // block
    $.ajax(
        {
            type: 'GET',
            async: false,
            url: 'api/region/',
            success: function(data) {
                var func_tmpl = _.template($('#region-tmpl').html());
                var all_region_html = "";
                for(var i=0; i<data.length;i++){
                    dict = {
                        url: '/api/region/'+data[i].id+'/cities/',
                        name: data[i].name
                    }
                    region_html = func_tmpl(dict);
                    all_region_html = all_region_html + region_html;
                }
                $('.dropdown-menu').html(all_region_html);
                $('li.region').on('click', function(e){
                    e.preventDefault();
                    var cities_url = $('a', e.currentTarget).attr("href");
                    var region_name = $('a', e.currentTarget).html();
                    $('#dropdownMenu1').html(region_name+'<span class="caret"></span>')

                    loadCities(cities_url);
                });
            },
        }
    );

    // unblock
}

function loadCities(cities_url) {
    // block
    $.ajax(
        {
            type: 'GET',
            async: false,
            url: cities_url,
            success: function(data) {
                chart_data = [{
                    key: "Population",
                    values: data
                }];
                drawChart(chart_data);
            },
        }
    );
    // unblock
}

function drawChart(data) {
    console.log(data);
    if (chart == null) {
        window.chart = nv.models.discreteBarChart()
            .x(function(d) { return d.name })
            .y(function(d) { return d.people })
            .staggerLabels(true)
            .tooltips(true)
            .showValues(true)
            .transitionDuration(350)
            ;

  
        nv.utils.windowResize(chart.update);
        nv.addGraph(chart);
    }
    d3.select('#chart svg')
      .datum(data)
      .call(chart);
}
