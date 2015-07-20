from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

register = template.Library()

@register.inclusion_tag('bootstrap_theme/fragments/header.html')
def header():
    return {'static_url':settings.STATIC_URL}

@register.simple_tag
def buttonlink(url, icn):
    return '<a class="btn btn-default" href="%s"><i class="glyphicon glyphicon-%s"></i></a>' % (url, icn)

@register.filter
def emphasis(value, arg=""):
    if arg == "":
        css = "muted"
    else:
        css = "text-%s" % arg
    return mark_safe('<p class="%s">%s</p>' % (css, value))

@register.filter
def abbrev(value, arg):
    return mark_safe('<abbr title="%s">%s</abbr>' % (value, arg))

@register.filter
def yesnoicon(value):
    icon = "ok" if value else "remove"
    return mark_safe('<i class="glyphicon glyphicon-%s"></i>' % icon)

@register.filter
def ratingicon(value):
    return mark_safe('<i class="glyphicon glyphicon-star"></i>' * value)

class NavbarNode(template.Node):
    def __init__(self, nodelist, site_title):
        self.nodelist = nodelist
        self.site_title = site_title
    def render(self, context):
        output = self.nodelist.render(context)
        if not (self.site_title[0] == self.site_title[-1] and self.site_title[0] in ('"', "'")):
            try:
                self.site_title = template.Variable(self.site_title).resolve(context)
            except template.VariableDoesNotExist:
                self.site_title = "Bootstrap"
        else:
            self.site_title = self.site_title[1:-1]
        return """
    <div class="navbar navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container">
          <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </a>
          <a class="brand" href="#">%s</a>
          <div class="nav-collapse">
            <ul class="nav">
            %s
            </ul>
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>
        """ % (self.site_title, output)

def do_navbar(parser, token):
    try:
        tag_name, site_title = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    nodelist = parser.parse(('endnavbar',))
    parser.delete_first_token()
    return NavbarNode(nodelist, site_title)

class ContainerNode(template.Node):
    def __init__(self, nodelist, base_class, option):
        self.nodelist = nodelist
        self.option = option
        self.base_class = base_class
    def render(self, context):
        output = self.nodelist.render(context)
        css = self.base_class if self.option == 'fixed' else '%s-fluid' % self.base_class
        return '<div class="%s">%s</div>' % (css, output)

def do_container(parser, token):
    try:
        tag_name, option = token.split_contents()
        if not (option[0] == option[-1] and option[0] in ('"', "'")):
            raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
        if option[1:-1] not in ('fixed', 'fluid'):
            raise template.TemplateSyntaxError("%r tag's argument should be either fixed or fluid" % tag_name)
    except ValueError:
        tag_name = "container"
        option = "'fixed'"
    nodelist = parser.parse(('endcontainer',))
    parser.delete_first_token()
    return ContainerNode(nodelist, 'container', option[1:-1])

def do_row(parser, token):
    try:
        tag_name, option = token.split_contents()
        if not (option[0] == option[-1] and option[0] in ('"', "'")):
            raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
        if option[1:-1] not in ('fixed', 'fluid'):
            raise template.TemplateSyntaxError("%r tag's argument should be either fixed or fluid" % tag_name)
    except ValueError:
        tag_name = "row"
        option = "'fixed'"
    nodelist = parser.parse(('endrow',))
    parser.delete_first_token()
    return ContainerNode(nodelist, 'row', option[1:-1])

class SpanNode(template.Node):
    def __init__(self, nodelist, size):
        self.nodelist = nodelist
        self.size = size
    def render(self, context):
        output = self.nodelist.render(context)
        return '<div class="span%d">%s</div>' % (self.size, output)

def do_span(parser, token):
    try:
        tag_name, size = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    if not (size[0] == size[-1] and size[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    size = int(size[1:-1])
    if size > 12:
        raise template.TemplateSyntaxError("%r tag's argument should be less than 12" % tag_name)
    nodelist = parser.parse(('endspan',))
    parser.delete_first_token()
    return SpanNode(nodelist, size)

class ToolbarNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
    def render(self, context):
        output = self.nodelist.render(context)
        return '<div class="btn-toolbar"><div class="btn-group">%s</div></div>' % output

def do_toolbar(parser, token):
    nodelist = parser.parse(('endtoolbar',))
    parser.delete_first_token()
    return ToolbarNode(nodelist)

class DropdownNode(template.Node):
    def __init__(self, nodelist, url, icn, text):
        self.nodelist = nodelist
        self.url = url
        self.icon = icn
        self.text = text
    def render(self, context):
        output = self.nodelist.render(context)
        return """<div class="btn-group">
<a class="btn btn-primary" href="%s"><i class="icon-%s icon-white"></i> %s</a>
<a class="btn btn-primary dropdown-toggle" data-toggle="dropdown" href="#"><span class="caret"></span></a>
<ul class="dropdown-menu">%s</ul></div>""" % (self.url, self.icon, self.text, output)

def do_dropdown(parser, token):
    try:
        tag_name, url, icn, text = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires 3 arguments" % token.contents.split()[0])
    if not (url[0] == url[-1] and url[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's first argument should be in quotes" % tag_name)
    if not (icn[0] == icn[-1] and icn[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's second argument should be in quotes" % tag_name)
    if not (text[0] == text[-1] and text[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's third argument should be in quotes" % tag_name)
    nodelist = parser.parse(('enddropdown',))
    parser.delete_first_token()
    return DropdownNode(nodelist, url[1:-1], icn[1:-1], text[1:-1])

register.tag('navbar', do_navbar)
register.tag('container', do_container)
register.tag('row', do_row)
register.tag('span', do_span)
register.tag('toolbar', do_toolbar)
register.tag('dropdown', do_dropdown)

@register.filter
def link(value, icon=None):
    icon_html = '<i class="glyphicon glyphicon-%s"></i>' % icon if icon else ''
    try:
        return mark_safe('<a href="%s">%s%s</a>' % (value.get_absolute_url(), icon_html, value))
    except:
        return value

@register.inclusion_tag('bootstrap_theme/fragments/carousel.html')
def carousel(group_name):
    return {'group_name': group_name, 'object_list': Carousel.objects.filter(carousel_group=group_name)}

@register.inclusion_tag('bootstrap_theme/fragments/navbar_gradient.css')
def navbar_gradient(first_color, last_color):
    return {'first_color': first_color, 'last_color': last_color}

class ModalNode(template.Node):
    def __init__(self, nodelist, *varlist):
        self.nodelist, self.vlist = (nodelist, varlist)
    def render(self, context):
        modal_id = 'myModal'
        form_action = None
        csrf_token = context.get('csrf_token', None)
        title = template.Variable(self.vlist[0]).resolve(context)
        if len(self.vlist) > 1:
            modal_id = template.Variable(self.vlist[1]).resolve(context)
        if len(self.vlist) > 2:
            form_action = template.Variable(self.vlist[2]).resolve(context)
        return render_to_string('bootstrap_theme/fragments/modal.html', {'modal_id': modal_id,
                                                                   'title': title,
                                                                   'body': self.nodelist.render(context),
                                                                   'form_action':form_action,
                                                                   'csrf_token':csrf_token})

@register.tag
def modal(parser, token):
    nodelist = parser.parse(('endmodal',))
    parser.delete_first_token()
    return ModalNode(nodelist, *token.split_contents()[1:])

@register.simple_tag
def icon(slug):
    return mark_safe('<i class="glyphicon glyphicon-%s"></i>' % slug)

@register.simple_tag
def modal_button(title, modal=None, icon=None):
    icon = '<i class="glyphicon glyphicon-%s"></i>' % icon if icon else ''
    if not modal:
        modal = 'myModal'
    return mark_safe('<a class="btn" role="button" href="#%s" data-toggle="modal">%s%s</a>' % (modal, icon, title))
