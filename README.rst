Viewed Records — Odoo 17 Module
===============================

Description
-----------

**Viewed Records** is a module designed to track which records users have opened 
across any Odoo model. It automatically saves a viewing history whenever a form is opened, 
allows checking whether a user has already viewed a record, and displays a 
"viewed" status directly on the form.

How It Works
------------

To enable tracking, a model must inherit the mixin::

    viewed.records.mixin

And the form must use the widget::

    js_class="viewed_records"

When a user opens a form, the module automatically creates an entry in 
``viewed.record.history`` and updates the boolean field ``is_viewed``.

Models
------

viewed.record.history
~~~~~~~~~~~~~~~~~~~~~

This model stores info about viewed records:

- **res_model** — model name  
- **record_id** — record ID  
- **user_id** — user  
- **record_name** — name of the record  
- **record_url** — URL to open the form  

viewed.records.mixin
~~~~~~~~~~~~~~~~~~~~

Enables any model to support viewed-record tracking.

Includes:

- **is_viewed** — Boolean, automatically computed  

JavaScript Widget
-----------------

The widget is activated in the form view::

    <form js_class="viewed_records">

It triggers the method ``mark_as_viewed()`` when the form loads.

Example
~~~~~~~

.. code-block:: xml

    <record id="view_task_form" model="ir.ui.view">
        <field name="name">project.task.form</field>
        <field name="model">project.task</field>
        <field name="arch" type="xml">
            <form js_class="viewed_records">
                <field name="name"/>
            </form>
        </field>
    </record>


Python Mixin
------------

.. code-block:: python

    class ViewedRecordsMixin(models.AbstractModel):
        _name = 'viewed.records.mixin'

        is_viewed = fields.Boolean(string='Is Opened', compute='_compute_is_viewed')

        @api.depends()
        def _compute_is_viewed(self):
            ViewedRecordsHistory = self.env['viewed.records.history']
            for rec in self:
                viewed = ViewedRecordsHistory.search([
                    ('res_model', '=', self._name),
                    ('record_id', '=', rec.id),
                    ('user_id', '=', self.env.user.id),
                ], limit=1)
                rec.is_viewed = bool(viewed)


Using the Mixin in a Model
--------------------------

To enable tracking in your model:

.. code-block:: python

    class ProjectTask(models.Model):
        _name = 'project.task'
        _inherit = ['project.task', 'viewed.records.mixin']

This adds:

- the ``is_viewed`` field  
- automatic history logging  
- ability to highlight unread records  

List View Decoration — Highlight Unread Records
-----------------------------------------------

The module supports highlighting records that the user has *not* viewed.

Example
~~~~~~~

.. code-block:: xml

    <record id="view_task_list" model="ir.ui.view">
        <field name="name">project.task.list</field>
        <field name="model">project.task</field>
        <field name="arch" type="xml">
            <list decoration-info="not is_viewed">
                <field name="name"/>
                <field name="is_viewed" column_invisible="1"/>
            </list>
        </field>
    </record>

Rows where ``is_viewed = False`` are shown with an **info** highlight.  
Useful for tasks, leads, tickets, documents and any workflow that benefits from “unread” tracking.


Installation
------------

Copy the module into your Odoo ``addons/`` directory and install it via the Apps menu.


Contact
-------

Author: **Saken Serdaly**  
Email: ``sakenever137@gmail.com``  
GitHub: https://github.com/sakenever137
