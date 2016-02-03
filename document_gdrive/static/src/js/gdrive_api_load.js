// # -*- coding: utf-8 -*-
// ##############################################################################
// #
// #    Copyright (c) 2015 be-cloud.be
// #                       Jerome Sonnet <jerome.sonnet@be-cloud.be>
// #
// #    This program is free software: you can redistribute it and/or modify
// #    it under the terms of the GNU Affero General Public License as
// #    published by the Free Software Foundation, either version 3 of the
// #    License, or (at your option) any later version.
// #
// #    This program is distributed in the hope that it will be useful,
// #    but WITHOUT ANY WARRANTY; without even the implied warranty of
// #    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// #    GNU Affero General Public License for more details.
// #
// #    You should have received a copy of the GNU Affero General Public License
// #    along with this program.  If not, see <http://www.gnu.org/licenses/>.
// #
// ##############################################################################

// The Client ID of Imply.lu

var scope = ['https://www.googleapis.com/auth/drive'];

var pickerApiLoaded = false;
var oauthToken = false;
var clientId = false;

function getClientId() {
      var P = new openerp.web.Model('ir.config_parameter');
      P.call('get_param', ['document.gdrive.client.id']).then(function(id) {
          clientId = id;
        }).fail(function(error) {
          console.log(error);
        });
}

// Use the API Loader script to load google.picker and gapi.auth.
function onApiLoad() {
  gapi.load('auth', {'callback': onAuthApiLoad});
  gapi.load('picker', {'callback': onPickerApiLoad});
}

function onAuthApiLoad() {
  if(!clientId) {getClientId();}
  window.gapi.auth.authorize(
      {
        'client_id': clientId,
        'scope': scope,
        'immediate': true,
        'include_granted_scopes' : true
      },
      handleAuthResult);
}

function onPickerApiLoad() {
  pickerApiLoaded = true;
}

function handleAuthResult(authResult) {
  if(!clientId) {getClientId();}
  if (authResult && !authResult.error) {
    oauthToken = authResult.access_token;
  } else {
	  window.gapi.auth.authorize(
      {
        'client_id': clientId,
        'scope': scope,
        'immediate': false,
        'include_granted_scopes' : true
      },
      handleAuthResult2);
  }
}

function handleAuthResult2(authResult) {
  if (authResult && !authResult.error) {
    oauthToken = authResult.access_token;
  } else {
	  alert("Cannot get authorization token for Google Drive: " + authResult.error_subtype + " - " + authResult.error);
  }
}  
	  
