
'content': 'data(name)',
'text-valign': 'top',
'color': 'white',
'text-outline-width': 1,
'text-outline-color': '#888',
'background-color': '#888'
})
.selector(':selected')
.css({
'background-color': 'black',
'line-color': 'black',
'target-arrow-color': 'black',
'source-arrow-color': 'black',
'text-outline-color': 'black',

})
.selector('edge')
.css({
'width':2,
'curve-style': 'bezier',
'target-arrow-color': '#888',
'target-arrow-shape': 'vee',
'line-color': 'grey',
'label': 'data(label)',
'color': 'white',
'text-outline-width': 2,
'text-outline-color': '#888'
}), 