// Search database for typeahead's suggestions
function search_all(query, syncResults, asyncResults) {
    // Get places matching query (asynchronously)
    let parameters = {
        q: query
    };
    $.getJSON("/search_all", parameters, function(data, textStatus, jqXHR) {

        // Call typeahead's callback with search results (i.e., names)
        asyncResults(data);
    });
}

// Configure application
function configure() {

    // Configure typeahead
    $("#q").typeahead({
        highlight: false,
        minLength: 1
    }, {
        display: function(suggestion) {
            return null;
        },
        limit: 3,
        source: search_all,
        templates: {
            suggestion: Handlebars.compile(
                "<div>" +
                "<a href=" +
                "'" +
                "{{website}}" +
                "'>" +
                "{{name}}" +
                "</a>" +
                "</div>"
            )
        }
    });
}

$(document).ready(configure)