


// ---------
// SVG SETUP
// ---------

var width = window.innerWidth * 5 / 6
var height = window.innerHeight * 5 / 6
var draw = SVG('drawing').size(width, height)
var library_data = {"australian dance": 24, "australian hip hop": 9, "australian indie": 10, "downtempo": 9, "edm": 494, "electronic trap": 172, "escape room": 20, "chillwave": 8, "ninja": 9, "tropical house": 170, "wave": 36, "bass trap": 147, "traprun": 51, "vapor twitch": 94, "emo rap": 40, "underground hip hop": 77, "canadian hip hop": 71, "vapor trap": 17, "experimental pop": 1, "indie garage rock": 4, "indie psych-rock": 8, "bedroom pop": 1, "indie r&b": 21, "norwegian indie": 1, "miami hip hop": 29, "indie surf": 2, "lo-fi beats": 21, "chillstep": 59, "substep": 13, "canadian contemporary r&b": 25, "canadian pop": 86, "pop": 553, "rap": 448, "destroy techno": 1, "electro house": 332, "deep underground hip hop": 34, "lancaster pa indie": 1, "boy band": 24, "hip hop": 351, "tropical pop edm": 54, "big room": 150, "house": 85, "progressive electro house": 121, "progressive house": 121, "tech house": 7, "indietronica": 33, "vapor soul": 44, "brostep": 209, "filthstep": 52, "pop rap": 393, "new orleans rap": 14, "trap music": 135, "catstep": 61, "complextro": 81, "tracestep": 33, "australian underground hip hop": 2, "atl hip hop": 63, "soul flow": 2, "drum and bass": 30, "k-indie": 1, "dance pop": 314, "post-teen pop": 77, "viral pop": 4, "alternative hip hop": 20, "bedroom soul": 5, "chillhop": 1, "electro": 25, "alternative r&b": 13, "dmv rap": 16, "deep pop r&b": 4, "r&b": 81, "trap soul": 12, "drill": 4, "southern hip hop": 100, "norwegian hip hop": 1, "norwegian pop": 2, "electropop": 67, "indie poptimism": 51, "bmore": 8, "moombahton": 31, "aussietronica": 15, "east coast hip hop": 16, "filter house": 7, "turntablism": 2, "gangster rap": 51, "adult standards": 3, "mellow gold": 3, "rock": 30, "soft rock": 3, "urban contemporary": 36, "acoustic pop": 3, "folk-pop": 8, "indie anthem-folk": 2, "indie folk": 4, "neo mellow": 38, "neo-singer-songwriter": 1, "la indie": 6, "detroit hip hop": 45, "g funk": 41, "west coast rap": 16, "chicago rap": 23, "conscious hip hop": 34, "boston hip hop": 1, "ambeat": 1, "jazz rap": 1, "underground rap": 4, "indie pop rap": 45, "portland hip hop": 4, "trap queen": 3, "atl trap": 3, "battle rap": 1, "hardcore hip hop": 4, "indie electro-pop": 8, "egyptian pop": 9, "lgbtq+ hip hop": 5, "electra": 8, "indie psych-pop": 1, "french indie pop": 3, "french indietronica": 3, "chanson": 1, "nu disco": 3, "bass music": 8, "deep house": 2, "future garage": 3, "electronic": 9, "zapstep": 32, "sunset lounge": 1, "hip pop": 16, "modern alternative rock": 13, "modern rock": 34, "australian electropop": 6, "deep tropical house": 11, "alternative emo": 1, "dreamo": 1, "progressive post-hardcore": 1, "canadian electropop": 3, "edmonton indie": 2, "grave wave": 2, "indie pop": 12, "metropopolis": 19, "shimmer pop": 8, "portland indie": 1, "uk alternative hip hop": 1, "alternative dance": 14, "brooklyn indie": 6, "garage rock": 5, "indie rock": 5, "neo-psychedelic": 4, "dance-punk": 7, "new rave": 9, "gauze pop": 4, "indie dream pop": 1, "alternative metal": 33, "nu metal": 26, "post-grunge": 47, "glitch": 10, "glitch hop": 46, "rap rock": 11, "south african rock": 1, "swedish electropop": 8, "deep big room": 66, "deep groove house": 6, "nu skool breaks": 1, "progressive trance": 23, "progressive trance house": 1, "trance": 29, "uplifting trance": 21, "deep melodic euro house": 1, "electropowerpop": 5, "emo": 8, "pop punk": 34, "pop rock": 50, "melodic metalcore": 1, "metalcore": 2, "screamo": 5, "australian alternative pop": 1, "indie cafe pop": 2, "art pop": 5, "neo soul": 11, "cali rap": 5, "permanent wave": 16, "german techno": 10, "stomp pop": 3, "vapor pop": 5, "etherpop": 4, "new wave pop": 2, "rap metal": 11, "nz pop": 2, "vocal trance": 6, "dirty south rap": 28, "latin": 13, "reggaeton": 3, "francoton": 1, "australian psych": 3, "psychedelic rock": 4, "afro house": 2, "kwaito house": 1, "south african pop": 2, "australian pop": 11, "dutch house": 17, "bass house": 3, "jump up": 9, "jungle": 4, "liquid funk": 20, "neurofunk": 9, "afrobeats": 3, "afropop": 3, "nigerian hip hop": 2, "breakbeat": 18, "darkstep": 1, "sky room": 9, "alternative rock": 12, "chamber pop": 3, "k-hop": 1, "korean pop": 1, "deep dance pop": 3, "swedish alternative rock": 1, "swedish indie pop": 1, "fidget house": 3, "shiver pop": 1, "album rock": 3, "classic rock": 3, "folk rock": 2, "piano rock": 16, "singer-songwriter": 1, "ccm": 3, "christian alternative rock": 7, "christian hip hop": 7, "christian music": 5, "worship": 3, "dubstep": 30, "crunk": 6, "memphis hip hop": 3, "deep pop edm": 2, "christian trap": 2, "deep liquid": 5, "lilith": 1, "funk metal": 5, "latin pop": 2, "mexican pop": 1, "tropical": 2, "cubaton": 1, "latin hip hop": 2, "art rock": 1, "christian rock": 6, "talent show": 2, "chicago house": 4, "vocal house": 6, "neon pop punk": 10, "trancecore": 2, "hyphy": 4, "italian hip hop": 1, "trap latino": 1, "dancehall": 3, "bulgarian hip hop": 4, "punk": 4, "west coast trap": 2, "finnish edm": 2, "scottish singer-songwriter": 1, "wonky": 6, "covertrance": 1, "toronto indie": 1, "polish post-rock": 1, "disco house": 4, "swiss indie": 1, "country rap": 3, "neo-synthpop": 3, "canadian indie": 1, "jam band": 1, "abstract hip hop": 2, "deep chiptune": 1, "irish rock": 2, "northern irish indie": 1, "pop house": 2, "deep southern trap": 2, "houston rap": 2, "miami bass": 1, "latin viral pop": 1, "swedish pop": 3, "swedish synthpop": 2, "bubblegum pop": 1, "glam rock": 1, "french shoegaze": 1, "melbourne bounce": 2, "dance rock": 1, "europop": 4, "new romantic": 1, "new wave": 1, "synthpop": 1, "mashup": 2, "candy pop": 5, "full on": 1, "reggae fusion": 5, "roots reggae": 1, "grime": 9, "hip house": 5, "canadian punk": 1, "canadian rock": 3, "pop emo": 12, "contemporary country": 2, "country": 1, "country dawn": 1, "country road": 1, "nintendocore": 1, "post-screamo": 1, "canadian contemporary country": 1, "azonto": 2, "desi": 3, "indian pop": 3, "bassline": 4, "nordic house": 1, "hands up": 1, "hardstyle": 2, "basshall": 1, "pinoy hip hop": 3, "reggae": 1, "uk hip hop": 3, "uk garage": 2, "zim hip hop": 1, "zimdancehall": 1, "danish pop": 1, "bubblegum dance": 1, "eurodance": 2, "scottish hip hop": 2, "pixie": 8, "malaysian pop": 1, "swedish idol pop": 2, "comic": 1, "indiecoustica": 1, "swedish soul": 1, "alternative pop rock": 5, "celtic rock": 6, "antiviral pop": 1, "otacore": 1, "chicano rap": 1, "riddim": 1, "soca": 1, "stomp and holler": 2, "lounge": 1, "ambient idm": 1, "dream pop": 1, "death core": 1, "432hz": 1, "experimental dubstep": 1, "christmas": 1, "jazz blues": 1, "soul": 1, "soul jazz": 1, "vocal jazz": 1, "swedish folk pop": 1, "dutch pop": 1, "big beat": 1, "blues-rock": 1, "modern blues rock": 1, "punk blues": 1, "britpop": 1, "madchester": 1, "canadian metal": 2}

song_titles = Object.keys(library_data)
data = []
for (i = 0; i < song_titles.length; i++) {
    data.push(library_data[song_titles[i]])
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
    draw_circle(points[i])
}

app = new Vue({
    el: '#app',
    data: {
        queue: []
    }
})

function draw_circle(point) {
    return draw.circle(point.r * 2).move(point.cx - point.r, point.cy - point.r).attr({fill: '#f06'})
}

function distance(a, b) {
    return Math.sqrt(Math.pow(a.cx - b.cx, 2) + Math.pow(a.cy - b.cy, 2))
}

function overlaps(point, points) {
    for (i = 0; i < points.length; i++) {
        test_point = points[i]
        if (distance(point, test_point) <= point.r + test_point.r) {
            return true
        }
    }
    return false
}
//$.ajax('/api/genre_count').done(function(data) { create_chart( //JSON.parse(data))})