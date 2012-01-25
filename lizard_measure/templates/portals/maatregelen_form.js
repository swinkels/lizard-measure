
{
    xtype: 'formautoload',
    layout: 'anchor',
    autoScroll: true,
    trackResetOnLoad: true,
    bodyPadding: '10 25 10 10',//padding on the right side 25 for scrollbar
    height: '100%',
    url: '/measure/api/measure/?_accept=application/json&include_geom=true&action=update',
    loadProxy: {
        url: '/measure/api/measure/',
        type: 'ajax',
        method: 'GET',
        reader: {
          root: 'data',
          type: 'json'
        },
        params: {
            include_geom: true,
            flat: false,
            _accept: 'application/json',
            object_id: {{ measure.id }}
        },
        success: function(form, action) {
            console.log('success gives:');
            console.log(arguments);
        },
        failure: function(form, action) {
            Ext.Msg.alert("Load failed", action.result.errorMessage);
        }
    },
    items:[
        {
            name: 'id',
            xtype: 'hiddenfield'
        },
        {
            fieldLabel: 'Ident',
            name: 'ident',
            width: 200,
            xtype: 'textfield',
            allowBlank: false
        },
        {
            fieldLabel: 'Titel',
            name: 'title',
            anchor: '100%',
            xtype: 'textfield',
            allowBlank: false
        },
        {
            fieldLabel: 'Onderdeel van maatregel',
            name: 'parent',
            displayField: 'name',
            valueField: 'id',
            xtype: 'combodict',
            forceSelection: false,
            store: {
                fields: ['id', 'name'],
                proxy: {
                    type: 'ajax',
                    url: '/measure/api/measure/?_accept=application%2Fjson&query=parent:None&size=id_name',
                    reader: {
                        type: 'json',
                        root: 'data'
                    }
                }
            }
        },
        {
            fieldLabel: 'KRW maatregel',
            name: 'is_KRW_measure',
            xtype: 'checkbox',
            inputValue: true,
            allowBlank: true
        },

        {
            fieldLabel: 'Focus maatregel',
            name: 'is_indicator',
            inputValue: true,
            xtype: 'checkbox',
            allowBlank: true
        },
        {
            fieldLabel: 'Beschrijving',
            name: 'description',
            grow: true,
            anchor: '100%',
            xtype: 'textareafield',
            allowBlank: true
        },
        {
            fieldLabel: 'Maatregel type',
            name: 'measure_type',
            displayField: 'name',
            valueField: 'id',
            xtype: 'combodict',
            store: {
                fields: ['id', 'name'],
                data: Ext.JSON.decode({% autoescape off %}'{{ measure_types }}'{% endautoescape %})
            },
            multiSelect: false,
            forceSelection: true,
            allowBlank: false,
            width: 300
        },
        {
            fieldLabel: 'Periode',
            name: 'period',
            displayField: 'name',
            valueField: 'id',
            xtype: 'combodict',
            store: {
                fields: ['id', 'name'],
                data: Ext.JSON.decode({% autoescape off %}'{{ periods }}'{% endautoescape %})
            },
            forceSelection: true,
            allowBlank: false,
            width: 300
        },

        {
            fieldLabel: 'Categoriën',
            name: 'categories',
            displayField: 'name',
            valueField: 'id',
            xtype: 'combodict',
            store: {
                fields: ['id', 'name'],
                data: Ext.JSON.decode({% autoescape off %}'{{ categories }}'{% endautoescape %})
            },
            multiSelect: true,
            forceSelection: true,
            allowBlank: false,
            width: 300
        },
        {
            fieldLabel: 'Waarde',
            name: 'value',
            xtype: 'numberfield',
            minValue: 0,
            allowBlank: true
        },
        {
            fieldLabel: 'Eenheid',
            name: 'unit',
            displayField: 'name',
            valueField: 'id',
            xtype: 'combodict',
            store: {
                fields: ['id', 'name'],
                data: Ext.JSON.decode({% autoescape off %}'{{ units }}'{% endautoescape %})
            },
            forceSelection: true,
            allowBlank: false,
            width: 300
        },
        {
            xtype:'fieldset',
            collapsible: true,
            title: 'Planning',
            collapsed: false,
            layout: 'anchor',
            defaults: {
                anchor: '100%'
            },
            items: [
            {
                xtype: 'tablefield',
                fieldLabel: 'planning en realisatie',
                name: 'status_moments',
                field_name: 'status',
                editable: true,
                extra_fields:[{
                    text: 'planning',
                    dataIndex: 'planning_date',
                    width:100,
                    xtype: 'datecolumn',
                    format:'d-m-Y',
                    field: {
                        xtype: 'datefield',
                        format: 'd-m-Y'
                    }
                },{
                    text: 'realisatie',
                    dataIndex: 'realisation_date',
                    width:100,
                    xtype: 'datecolumn',
                    format:'d-m-Y',
                    field: {
                        xtype: 'datefield',
                        format: 'd-m-Y'
                    }
                }]

            },
            {
                fieldLabel: 'Aggregatie',
                name: 'aggregation_type',
                queryMode: 'local',
                displayField: 'name',
                valueField: 'id',
                xtype: 'combodict',
                store: {
                    fields: ['id', 'name'],
                    data: Ext.JSON.decode({% autoescape off %}'{{ aggregations }}'{% endautoescape %}),
                },
                forceSelection: true,
                allowBlank: false
            }
        ]
        },
        {
            xtype:'fieldset',
            collapsible: true,
            title: 'Organisaties en kosten',
            collapsed: false,
            layout: 'anchor',
            defaults: {
                anchor: '100%'
            },
            items: [
            {
                fieldLabel: 'Initiatiefnemer',
                name: 'initiator',
                displayField: 'name',
                valueField: 'id',
                xtype: 'combodict',
                forceSelection: true,
                store: {
                    fields: ['id', 'name'],
                    proxy: {
                        type: 'ajax',
                        url: '/measure/api/organization/?_accept=application%2Fjson&size=id_name',
                        reader: {
                            type: 'json',
                            root: 'data'
                        }
                    }
                }
            },
            {
                fieldLabel: 'Afdeling',
                name: 'responsible_department',
                xtype: 'textfield',
                allowBlank: true
            },
            {
                xtype: 'combodict',
                fieldLabel: 'Uitvoerder',
                name: 'executive',
                displayField: 'name',
                valueField: 'id',
                forceSelection: true,
                store: {
                    fields: ['id', 'name'],
                    proxy: {
                        type: 'ajax',
                        url: '/measure/api/organization/?_accept=application%2Fjson&size=id_name',
                        reader: {
                            type: 'json',
                            root: 'data'
                        }
                    }
                }
            },
            {
                fieldLabel: 'Totale kosten',
                name: 'total_costs',
                minValue: 0,
                allowDecimals: false,
                xtype: 'numberfield'
            },
            {
                fieldLabel: 'Investeringskosten',
                name: 'investment_costs',
                minValue: 0,
                allowDecimals: false,
                xtype: 'numberfield'
            },
            {
                fieldLabel: 'Exploitatiekosten',
                name: 'exploitation_costs',
                minValue: 0,
                allowDecimals: false,
                xtype: 'numberfield'
            },
            {
                xtype: 'combomultiselect',
                fieldLabel: 'Kosten verdeling organisaties',
                name: 'funding_organizations',
                read_at_once: true,
                editable: true,
                extra_fields:[{
                    text: 'percentage',
                    dataIndex: 'percentage',
                    width:100,
                    field: {
                        xtype:'numberfield',
                        step:1,
                        allowDecimals: false,
                        maxValue: 100,
                        minValue: 0
                    }
                }],
                combo_store: {
                    fields: [
                        {name: 'id', mapping: 'id'},
                        {name: 'percentage', mapping: 'percentage', defaultValue: 0},
                        {name: 'name', mapping: 'name'}
                    ],
                    proxy: {
                        type: 'ajax',
                        url: '/measure/api/organization/?_accept=application%2Fjson&size=id_name',
                        reader: {
                            type: 'json',
                            root: 'data'
                        }
                    }
                }
            }]
        },
        {
            xtype:'fieldset',
            collapsible:true,
            title: 'Link naar aan/afvoergebied en/of KRW-waterlichaam',
            collapsed: false,
            layout: 'anchor',
            defaults: {
                anchor: '100%'
            },
            items :[
            {
                xtype: 'combomultiselect',
                fieldLabel: 'aan/ afvoer gebieden',
                name: 'areas',
                field_name: 'aan/ afvoer gebieden',
                read_at_once: false,
                combo_store: {
                    fields: [
                        {name: 'id', mapping: 'id' },
                        {name: 'name', mapping: 'name' }
                    ],
                    proxy: {
                        type: 'ajax',
                        url: '/area/api/catchment-areas/?node=root&_accept=application%2Fjson&size=id_name',
                        reader: {
                            type: 'json',
                            root: 'areas'
                        }
                    }
                }
            }, {
                xtype: 'combomultiselect',
                fieldLabel: 'KRW waterlichamen',
                name: 'waterbodies',
                field_name: 'KRW waterlichamen',
                read_at_once: false,
                combo_store: {
                    fields: [
                        {name: 'id', mapping: 'id' },
                        {name: 'name', mapping: 'name' }
                    ],
                    proxy: {
                        type: 'ajax',
                        url: '/area/api/krw-areas/?node=root&_accept=application%2Fjson&size=id_name',
                        reader: {
                            type: 'json',
                            root: 'areas'
                        }
                    }
                }
            }]
        },
        {
            fieldLabel: 'Geometrie',
            name: 'geom',
            grow: true,
            anchor: '100%',
            xtype: 'textareafield',
            allowBlank: true
        },
        {
            xtype:'fieldset',
            collapsible:true,
            title: 'Metadata',
            collapsed: true,
            layout: 'anchor',
            defaults: {
                anchor: '100%'
            },
            items :[
            {
                fieldLabel: 'Alleen lezen',
                name: 'read_only',
                xtype: 'displayfield'

            },
            {
                fieldLabel: 'Bron',
                name: 'import_source',
                xtype: 'displayfield'
            },
            {
                fieldLabel: 'Ruwe data bron',
                name: 'import_raw',
                xtype: 'displayfield'
            }
            ]
        }
    ],
    buttons:[
    {
        text: 'Annuleren',
        handler: function() {
            this.up('window').close();
        }
    },{
        text: 'Opslaan',
        formBind: true, //only enabled once the form is valid
        //disabled: true,
        handler: function() {
            var form = this.up('form').getForm();
            var form_window = this.up('window')
            if (form.isValid()) {
                /* todo: de waarden zelf gaan rangschikken en verzenden */
                var values = form.getValues()

                if (!values['is_KRW_measure']) {
                    values['is_KRW_measure'] = false

                }
                if (!values['is_indicator']) {
                    values['is_indicator'] = false
                }

                Ext.MessageBox.show({
                    title: 'Wijzigingen opslaan',
                    msg: 'Samenvatting',
                    width: 300,
                    multiline: true,
                    buttons: Ext.MessageBox.OKCANCEL,
                    fn: function (btn, text) {
                        if (btn=='ok') {
                            values.edit_summary
                            Ext.Ajax.request({
                                url: '/measure/api/measure/?action=update&_accept=application/json&flat=false',
                                params: {
                                    object_id: values.id,
                                    edit_message: text,
                                    data:  Ext.JSON.encode(values)
                                },
                                method: 'POST',
                                success: function(xhr) {
                                    Ext.Msg.alert("Opgeslagen", "Opslaan gelukt");
                                },
                                failure: function(xhr) {
                                    Ext.Msg.alert("portal creation failed", "Server communication failure");
                                }
                            });
                        }
                    }
                })
            }
        }
    }]
}