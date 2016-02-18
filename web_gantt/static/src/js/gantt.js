odoo.define('web_gantt.GanttView', function (require) {
"use strict";

var core = require('web.core');
var data = require('web.data');
var form_common = require('web.form_common');
var Model = require('web.DataModel');
var time = require('web.time');
var View = require('web.View');
var widgets = require('web_calendar.widgets');

var CompoundDomain = data.CompoundDomain;

var _t = core._t;
var _lt = core._lt;
var QWeb = core.qweb;

var GanttView = View.extend({
  template: 'GanttView',
  display_name: _lt('Gantt'),

  init: function(parent, dataset, view_id, options) {
    this._super(parent, dataset, view_id, options);

    this.shown = $.Deferred();
    this.model = dataset.model;
    this.fields_view = {};
    this.view_type = 'gantt';

    this.title = (this.options.action)? this.options.action.name : '';
  },

  view_loading: function(fields_view) {
    var attrs = fields_view.arch.attrs;
    this.fields_view = fields_view;

    if (!attrs.date_start) {
      throw new Error(_t("Gantt view has not defined 'date_start' attribute."));
    }

    this.$el.addClass(attrs['class']);

    this.name = fields_view.name || attrs.string;
    this.view_id = fields_view.view_id;

    this.date_start = attrs.date_start;
    this.date_delay = attrs.date_delay;
    this.date_stop = attrs.date_stop;
    this.progress = attrs.progress;
    this.default_group_by = attrs.default_group_by;

    this.data = false;

    this.shown.done(this.shown_done.bind(this));
  },

  //called when view is shown
  shown_done: function() {
    this.trigger('gantt_view_loaded', this.fields_view);
  },

  do_show: function() {
    var self = this;
    this.shown.resolve();
    return this._super();
  },

  do_search: function(domain, context, group_by) {
    var self = this;
    this.shown.done(function () {
      self._do_search(domain, context, group_by);
    });
  },

  //do reading and rendering here
  _do_search: function(domain, context, group_by) {
    var self = this;

    if (this.data) {
      console.log('Consecutive ``do_search`` called. Cancelling.');
      return;
    }
    this.data = true;

    //get all fields in in <gantt/>
    var fields = _.compact(_.map(['date_start', 'date_delay', 'date_stop', 'progress', 'default_group_by'], function(key) {
      return self.fields_view.arch.attrs[key] || '';
    }));

    self.dataset.read_slice(fields, {
      offset: 0,
      domain: domain,
      context: context
    }).done(this.read_slice_done.bind(this)).fail(function () {
      self.data = false;//do not leave in a undefined state
    });
  },

  read_slice_done: function(data) {
    var self = this;

    this.data = data;

    this.dataset.name_get(_.map(data, function(object) {
      return object.id;
    })).done(this.name_get_done.bind(this)).fail(function () {
      self.data = false;//do not leave in a undefined state
    });
  },

  name_get_done: function(names) {
    //transform this.data previously gathered in this.read_slice_done
    //into a format readable by the gantt library
    this.init_gantt(this.transform_data(names));
  },

  init_gantt: function(source) {
    $('.o_gantt_widget').gantt({
      source: source,
      scale: "days",
      navigate: "scroll",
      minScale: "days",
      maxScale: "months",
      itemsPerPage: 100
    });

    this.data = false;//reset
  },

  transform_data: function(names) {
    var self = this;

    var rows = _.map(this.data, function(object) {
      var date_start = object[self.date_start];
      var date_stop = object[self.date_stop] || date_start;
      var desc = _.find(names, function(tuple) { return tuple[0] == object.id; })[1];

      var name = object[self.default_group_by] || ' ';
      if (Object.prototype.toString.call(name) == '[object Array]') {
        //Many2one
        name = name[1];
      }

      return {
        name: name,
        desc: desc,
        values: [{
          from: Date.parse(date_start),
          to: Date.parse(date_stop)
        }]
      };
    });

    var grouped = _.groupBy(rows, 'name');
    var final = [];

    _.each(grouped, function(group, group_name) {
      var date_start = _.min(group, function(element) {
        return element.values[0].from;
      }).values[0].from;
      var date_end = _.max(group, function(element) {
        return element.values[0].to;
      }).values[0].to;

      final.push({
        name: group_name,
        values: [{
          from: date_start,
          to: date_end,
          customClass: 'ganttOrange'
        }]
      });

      group = _.map(group, function(element) {
        element.name = ' ';
        return element;
      });

      Array.prototype.push.apply(final, group);
    });

    return final;
  }
});

core.view_registry.add('gantt', GanttView);

return GanttView;
});
