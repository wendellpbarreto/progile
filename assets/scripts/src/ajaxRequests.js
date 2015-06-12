$(function() {
	String.prototype.decodeHTML = function() { return $("<div>", {html: "" + this}).html(); };

	var $page = $("#page"), $preloader = $("#preloader"), $counter = 0;

	checkUrl = function(slug) {
		var url = location.href;
		var regex = '^(http[s]?\:\/\/){0,1}(www\.){0,1}[a-zA-Z0-9\.\-\_\:]+(\/)?' + slug + '(\#)?(\/)?$';
		if (url.match(new RegExp(regex))) { return true; } else { return false; };
	},

	engineSideMenu = function() {

	},

	engineFormValidations = function() {
	},

	engineGraphs = function(graph, resource, title) {

	},

	enginePage = function() {
		$(document).foundation({});

		if (checkUrl("boards/[0-9]+")) {
			console.log('[INFO] enginePage called at: boards/[0-9]+.');

			var el = document.getElementById('boards');
			var sortable = new Sortable(el, {
			    group: { name: "boards", pull: true, put: true },  // or { name: "...", pull: [true, false, clone], put: [true, false, array] }
			    sort: true,  // sorting inside list
			    delay: 0, // time in milliseconds to define when the sorting should start
			    disabled: false, // Disables the sortable if set to true.
			    store: null,  // @see Store
			    animation: 150,  // ms, animation speed moving items when sorting, `0` — without animation
			    handle: ".board__header",  // Drag handle selector within list items
			    filter: ".ignore-elements",  // Selectors that do not lead to dragging (String or Function)
			    draggable: ".board",  // Specifies which items inside the element should be sortable
			    ghostClass: "sortable-ghost",  // Class name for the drop placeholder
			    dataIdAttr: 'data-id',

			    scroll: true, // or HTMLElement
			    scrollSensitivity: 30, // px, how near the mouse must be to an edge to start scrolling.
			    scrollSpeed: 10, // px

			    // Called by any change to the list (add / update / remove)
			    onSort: function (/**Event*/evt) {
			        // same properties as onUpdate
			        console.log(evt);

			        $('.board').each(function(index, el) {
			            $.get( "http://127.0.0.1:8000/update_board", { board_id: el.dataset.boardId, order: index } )
			        });
			    },

			});


			[].forEach.call(el.getElementsByClassName('board__tasks'), function (el){
			    Sortable.create(el, {
			        group: 'board__task',
			        ghostClass: "board__task-ghost",  // Class name for the drop placeholder
			        animation: 150,
			        filter: ".disabled",

			        // Element is dropped into the list from another list
			        onAdd: function (/**Event*/evt) {
			            console.log(evt);
			            var itemEl = evt.item;  // dragged HTMLElement
			            evt.from;  // previous list
			            // + indexes from onEnd

			            boardTarget = $(itemEl).closest(".board__tasks");
			            console.log((itemEl).closest(".board__tasks"));

			            $.get( "http://127.0.0.1:8000/update_task", { task_id: itemEl.dataset.taskId, board_id: boardTarget[0].dataset.fromBoard } )
			            // .done(function( data ) {
			            //     console( "Data Loaded: " + data );
			            // });
			        },
			    });
			});

		} else if (checkUrl("sprints/[0-9]+")) {
			console.log('[INFO] enginePage called at: sprints/[0-9]+.');

			$('.datepicker').pickadate({
		        formatSubmit: 'yyyy/mm/dd',
		    });

			var el = document.getElementById('board-sprints');
			var sortable = new Sortable(el, {
			    group: { name: "boards", pull: true, put: true },  // or { name: "...", pull: [true, false, clone], put: [true, false, array] }
			    sort: true,  // sorting inside list
			    delay: 0, // time in milliseconds to define when the sorting should start
			    disabled: false, // Disables the sortable if set to true.
			    store: null,  // @see Store
			    animation: 150,  // ms, animation speed moving items when sorting, `0` — without animation
			    handle: ".board__header",  // Drag handle selector within list items
			    filter: ".ignore-elements",  // Selectors that do not lead to dragging (String or Function)
			    draggable: ".board",  // Specifies which items inside the element should be sortable
			    ghostClass: "sortable-ghost",  // Class name for the drop placeholder
			    dataIdAttr: 'data-id',

			    scroll: true, // or HTMLElement
			    scrollSensitivity: 30, // px, how near the mouse must be to an edge to start scrolling.
			    scrollSpeed: 10, // px

			    // Called by any change to the list (add / update / remove)
			    onSort: function (/**Event*/evt) {
			        // same properties as onUpdate

			        $('.board').each(function(index, el) {
			            $.get( "http://127.0.0.1:8000/update_board", { board_id: el.dataset.boardId, order: index } )
			        });
			    },

			});


			[].forEach.call(el.getElementsByClassName('tasks'), function (el){
			    Sortable.create(el, {
			        group: 'task',
			        ghostClass: "board__task-ghost",  // Class name for the drop placeholder
			        animation: 150,
			        filter: ".disabled",

			        // Element is dropped into the list from another list
			        onAdd: function (/**Event*/evt) {
			            console.log(evt);
			            var itemEl = evt.item;  // dragged HTMLElement
			            evt.from;  // previous list
			            // + indexes from onEnd
			           	
			           	if ($(evt.target).attr('data-sprint-id')) {
				            $.get( "http://127.0.0.1:8000/update_task", { task_id: itemEl.dataset.taskId, sprint_id: evt.target.dataset.sprintId, order: evt.newIndex } )
			           	} else {
			           		$.get( "http://127.0.0.1:8000/update_task", { task_id: itemEl.dataset.taskId, sprint_id: 0 } )
			           	}
			        },
			        onSort: function (/**Event*/evt) {
				        // same properties as onUpdate
			           	$('.sprints .sprint .task').each(function(index, el) {
				            $.get( "http://127.0.0.1:8000/update_task", { task_id: el.dataset.taskId, order: index } )
				        });
				    },

			    });
			});

		} else {
			console.log('[INFO] enginePage called at generic page.');

			if ($('table#dashboard-simulated-test-graph-resource').length > 0) {
				var resource = $('table#dashboard-simulated-test-graph-resource tr').get().map(function(row) {
					return $(row).find('td').get().map(function(cell) {
						return $(cell).html();
					});
				});

				categories = [];
				for (i = 2; i < resource.length; ++i) {
					categories.push(resource[i][0]);
				}
				data = [];
				for (j = 1; j < resource[0].length; ++j) {
					data[j-1] = {};
					data[j-1]["data"] = [];
					data[j-1]["name"] = resource[0][j];
					data[j-1]["color"] = resource[1][j];

					for (k = 2; k < resource.length; ++k) {
						data[j-1]["data"].push(parseFloat(resource[k][j]));
					}
				}

				$('#dashboard-simulated-test-graph').highcharts({
					chart: {
						type: 'column',
						height: 220,
					},
					title: { text: ' '  },
					legend: {
						layout: 'horizontal',
						align: 'center',
						verticalAlign: 'top',
					},
					credits: false,
					xAxis: {
						categories: categories,
						crosshair: true
					},
					yAxis: {
						min: 0,
						max: 100,
						tickInterval: 20,
						title: {
							text: 'Porcentagem de acertos'
						}
					},
					tooltip: {
						headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
						pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
						'<td style="padding:0"><b>{point.y:.1f} %</b></td></tr>',
						footerFormat: '</table>',
						shared: true,
						useHTML: true
					},
					plotOptions: {
						column: {
							pointPadding: 0.2,
							borderWidth: 0
						}
					},
					series: data
				});
			}

			if ($('#flot-chart1').length > 0) {
				var d1 = [[1262304000000, 6], [1264982400000, 3057], [1267401600000, 20434], [1270080000000, 31982], [1272672000000, 26602], [1275350400000, 27826], [1277942400000, 24302], [1280620800000, 24237], [1283299200000, 21004], [1285891200000, 12144], [1288569600000, 10577], [1291161600000, 10295]];
				var d2 = [[1262304000000, 5], [1264982400000, 200], [1267401600000, 1605], [1270080000000, 6129], [1272672000000, 11643], [1275350400000, 19055], [1277942400000, 30062], [1280620800000, 39197], [1283299200000, 37000], [1285891200000, 27000], [1288569600000, 21000], [1291161600000, 17000]];

				var data1 = [
				{ label: "Data 1", data: d1, color: '#17a084'},
				{ label: "Data 2", data: d2, color: '#127e68' }
				];
				$.plot($("#flot-chart1"), data1, {
					xaxis: {
						tickDecimals: 0
					},
					series: {
						lines: {
							show: true,
							fill: true,
							fillColor: {
								colors: [{
									opacity: 1
								}, {
									opacity: 1
								}]
							},
						},
						points: {
							width: 0.1,
							show: false
						},
					},
					grid: {
						show: false,
						borderWidth: 0
					},
					legend: {
						show: false,
					}
				});
			}
		}
	},

	init = function() {
		engineSideMenu();
		enginePage();
		engineFormValidations();
	},

	ajaxLoad = function(html, status, xhr) {
		$counter++;
		console.log("- -- --- ---- ----- " + $counter + "º ajax call ----- ---- --- -- -");
		console.log("[INFO] Ajax Request Status: " + status);
		console.log("[INFO] Ajax Request XHR: " + xhr);
		if ( status == "error" ) {
			var msg = "Sorry but there was an error: ";
			alert(msg + xhr.status + " " + xhr.statusText);
		} else {
			// $preloader.hide( 500 );
			document.title = html
			.match(/<title>(.*?)<\/title>/)[1]
			.trim()
			.decodeHTML();
			init();
		}
	},

	loadPage = function(href) {
		$page.load(href + ' #page>*', ajaxLoad);
	};

	init();

	$(window).on("popstate", function(e) {
		if (e.originalEvent.state !== null) {
			loadPage(location.href);
		}
	});

	$(document).on("click", "a, [data-href]", function(ev) {
		var href = $(this).attr("href");
		var dataAjax = $(this).attr("data-ajax");

		if (dataAjax == "false" || href == undefined || href == '#') { return; }

		ev.preventDefault();

		if (href.indexOf(document.domain) > -1 || href.indexOf(':') === -1) {
			// $preloader.show( 500 );
			history.pushState({}, '', href);
			loadPage(href);
			return false;
		} else {
			console.log('[INFO] At: click.data-ajax');
		}
	});
});
