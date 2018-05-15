//api.js
//Handles all api requests to server.
const api = (function() {
    BASE_URL = 'http://localhost:5000';
    const getBookmarks = function(callback) {
        $.getJSON(BASE_URL + '/get', callback);
    }
    const createBookmark = function(bookmark, callback) {
        $.ajax({
            url: BASE_URL + '/post',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(bookmark),
            success: callback
        }) 
    }
    const updateBookmark = function(id, updateData, callback){
        $.ajax({
            url: BASE_URL + '/patch/' + id,
            method: 'PATCH',
            contentType: 'application/json',
            data: JSON.stringify(updateData),
            success: callback
        })
    }
    const deleteBookmark = function(id, callback){
        $.ajax({
            url: BASE_URL + '/delete/' + id,
            method: 'DELETE',
            contentType: 'application/json',
            success: callback
        })
    }
    return {
        getBookmarks,
        createBookmark,
        updateBookmark,
        deleteBookmark
    }
}());