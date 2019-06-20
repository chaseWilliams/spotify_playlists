
url_params = new URLSearchParams(window.location.search)
// -----
// vuejs
// -----

var app = new Vue({
    el: '#app',
    data: {
        genre_query: '',
        artist_query: '',
        selected_circles: [],
        all_circles: [],
        artist_query_matches: [],
        selected_artist: {}
    },
    created: function () {
        this.debounced_search_artist = _.debounce(this.search_artist, 500)
    },
    watch: {
        artist_query: function () {
            if (this.artist_query != '') {
                this.debounced_search_artist()
            }
        }
    },
    methods: {
        create_playlist: function () {
            $.ajax('/api/create_playlist?u=' + url_params.get('u') + '&genres=' + encodeURIComponent(this.genres_string_list))
        },
        // set all circles back to pink, remove from circles array
        unselect_genres: function () {
            var limit = this.selected_circles.length
            for (var i = 0; i < limit; i++) {
                this.selected_circles[0].toggle_select()
            }
            console.log(this.selected_circles)
            this.selected_circles = [];
        },
        // TODO: 
        // doesn't change color of the respective circle
        select_genre: function (genre) {
            for (var i = 0; i < this.all_circles.length; i++) {
                var circle = this.all_circles[i]
                if (circle.genre === genre) {
                    circle.toggle_select()
                    break
                }
            }
        },
        search_artist: function () {
            console.log('search artist called')
            $.ajax('/api/search_artist?q=' + this.artist_query).done(function (data) {
                app.$set(app, 'artist_query_matches', JSON.parse(data))
            })
        },
        select_artist: function (artist) {
            this.selected_artist = artist
        },
        add_selected_circle: function (circle) {
            this.selected_circles.push(circle)
        },
        remove_selected_circle: function (circle) {
            for (var i = 0; i < this.selected_circles.length; i++) {
                if (this.selected_circles[i] == circle) {
                    this.selected_circles.splice(i, 1)
                    break
                }
            }
        }
    },
    computed: {
        genres_display: function () {
            var str = '';
            for (var i = 0; i < this.selected_circles.length; i++) {
                str += this.selected_circles[i].genre + ', '
            }
            return str.substring(0, str.length - 2)
        },
        genres_string_list: function () {
            var str = '';
            for (var i = 0; i < this.selected_circles.length; i++) {
                str += this.selected_circles[i].genre + ','
            }
            return str.substring(0, str.length - 1)
        },
        genre_matches: function () {
            var matches = []
            for (var i = 0; i < this.all_circles.length; i++) {
                var genre = this.all_circles[i].genre
                if (genre.includes(this.genre_query)) {
                    matches.push(genre)
                }
            }
            matches.sort()
            return matches
        },
        artist_query_match_names: function () {
            console.log('called query match names')
            var matches = []
            for (var i = 0; i < this.artist_query_matches.length; i++) {
                matches.push(this.artist_query_matches[i].name)
            }
            return matches
        }
    }
})


// ---------
// SVG SETUP
// ---------

var width = window.innerWidth * 2 / 3
var height = window.innerHeight * 9 / 10
var draw = SVG('drawing').size(width, height)

// -------------------------------------------------
// MAIN
// this actually calls the API and constructs visual
// -------------------------------------------------
$.ajax('/api/genre_count?u=' + url_params.get('u')).done(function(data) { create_visual(JSON.parse(data))})

//-----------------------------------------
// this massive function creates the visual
// ----------------------------------------

function create_visual(library_data) {
    genres = Object.keys(library_data)
    data = []
    for (i = 0; i < genres.length; i++) {
        data.push(library_data[genres[i]])
    }

    var min = Infinity, max = -1
    for (i = 0; i < data.length; i++) {
        if (data[i] < min) {
            min = data[i]
        } else if (data[i] > max) {
            max = data[i]
        }
    }

    var scale = d3.scaleLog().domain([min, max]).range([1, 4]) // range 1-4 is temporary, will be scaled later to fit viewport
    var points = []
    points.push({
        cx: 0,
        cy: 0,
        r: scale(data[0])
    })
    for (i = 1; i < data.length; i++) {
        var radius = scale(data[i])
        var new_point = {r: radius}
        do {
            direction = Math.random() * Math.PI * 2
            random_point = points[Math.floor(Math.random() * points.length)]
            new_point.cx = random_point.cx + Math.cos(direction) * (radius + random_point.r)
            new_point.cy = random_point.cy + Math.sin(direction) * (radius + random_point.r) 
        } while (overlaps(new_point, points))
        points.push(new_point)
    }
    // transform and scale circles
    var min_x = Infinity, min_y = Infinity, max_x = -Infinity, max_y = -Infinity
    // figure out the bounds of current area
    for (i = 0; i < points.length; i++) {
        var point = points[i]
        if (point.cx - point.r < min_x) {
            min_x = point.cx - point.r
        }
        if (point.cy - point.r < min_y) {
            min_y = point.cy - point.r
        }
        if (point.cx + point.r > max_x) {
            max_x = point.cx + point.r
        }
        if (point.cy + point.r > max_y) {
            max_y = point.cy + point.r
        }
    }

    // transform bounds to viewport (all x's and y's are positive)
    // min_x and min_y are certainly negative
    for (i = 0; i < points.length; i++) {
        var point = points[i]
        point.cx -= min_x
        point.cy -= min_y
    }
    max_x -= min_x
    max_y -= min_y

    console.log(points)
    // figure out ratio of area size to viewport size
    ratio_x = width / max_x
    ratio_y = height / max_y
    ratio = ratio_x < ratio_y ? ratio_x : ratio_y
    origin = {cx: 0, cy: 0, r:1}
    // scale area size to viewport
    for (i = 0; i < points.length; i++) {
        var point = points[i]
        // move all points along the line from (0,0) to their respective coordinates
        // this will perform a dilation or compression on all the points
        point.cx *= ratio
        point.cy *= ratio
        point.r *= ratio
    }
    // finally draw the circles
    for (i = 0; i < points.length; i++) {
        draw_circle(points[i], genres[i])
    }
}

// ---------------------------
// additional helper functions
// ---------------------------

// sets up the circle
function draw_circle(point, genre) {
    var _circle = draw.circle(point.r * 2).move(point.cx - point.r, point.cy - point.r).attr({fill: '#f06'})
    _circle.genre = genre
    _circle.selected = false
    _circle.toggle_select = function() {
        console.log(this.genre)
        if (this.selected === true) {
            this.fill({color: '#f06'})
            this.selected = false
            app.remove_selected_circle(this)
        } else {
            this.fill({color: '#000'})
            this.selected = true
            app.add_selected_circle(this)
        }
    }
    _circle.mouseover(function() {
        if (!this.selected)
            this.fill({ color: '#000' })
    })
    _circle.mouseout(function() {
        if (!this.selected)
            this.fill({color: '#f06'})
    })
    _circle.click(function() {
        this.toggle_select()
      })
    app.all_circles.push(_circle)
    return _circle
}

function distance(a, b) {
    return Math.sqrt(Math.pow(a.cx - b.cx, 2) + Math.pow(a.cy - b.cy, 2))
}

function overlaps(point, points) {
    for (i = 0; i < points.length; i++) {
        test_point = points[i]
        if (distance(point, test_point) < point.r + test_point.r) {
            return true
        }
    }
    return false
}
