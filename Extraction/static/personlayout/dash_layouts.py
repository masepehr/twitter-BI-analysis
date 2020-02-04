from dash.base import BaseDashboardLayout, BaseDashboardPlaceholder
from dash.base import layout_registry
class PersonMainPlaceholder(BaseDashboardPlaceholder):

    uid = 'main'  # Unique ID of the placeholder.
    cols = 6  # Number of columns in the placeholder.
    rows = 4  # Number of rows in the placeholder.
    cell_width = 180  # Width of a single cell in the placeholder.
    cell_height = 180 # Height of a single cell in the placeholder.


class PersonLayout(BaseDashboardLayout):

    uid = 'personal'  # Layout UID.
    name = 'Personal'  # Layout name.

    # View template. Master template used in view mode.
    view_template_name = 'personal/view_layout.html'

    # Edit template. Master template used in edit mode.
    edit_template_name = 'personal/edit_layout.html'

    # All placeholders listed. Note, that placeholders are rendered in the
    # order specified here.
    placeholders = [PersonMainPlaceholder]

    # Cell units used in the entire layout. Allowed values are: 'px',
    # 'pt', 'em' or '%'. In the ``ExampleMainPlaceholder`` cell_width is
    # set to 150. It means that in this particular case its' actual width
    # would be `150px`.
    cell_units = 'px'

    # Layout specific CSS.
    media_css = ('css/dash_layout_personal.css',)

    # Layout specific JS.
    media_js = ('js/dash_layout_personal.js',)

# Registering the layout.
layout_registry.register(PersonLayout)