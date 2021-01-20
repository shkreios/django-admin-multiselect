from django.utils.safestring import mark_safe
from django import forms


class DjangoAdminMultiselect(forms.SelectMultiple):
    class Media:
        extend = False
        css = {
            'all': ('css/django-admin-multiselect.css',)
        }
        js = ('js/django-admin-multiselect.js', )

    def render(self, name, value, attrs=None, choices=()):
        output = super(DjangoAdminMultiselect, self).render(name, value, attrs, choices)
        output += u'''
        	<script type="text/javascript">
		(function($) {
			var el = $('#id_%s');
			var el_id = el.attr('id');
			var options = {
				 selectableHeader: "<input type='text' class='search-input' autocomplete='off' placeholder='search available'>",
				  selectionHeader: "<input type='text' class='search-input' autocomplete='off' placeholder='search selected'>",
				  afterInit: function(ms){
				    var that = this,
					$selectableSearch = that.$selectableUl.prev(),
					$selectionSearch = that.$selectionUl.prev(),
					selectableSearchString = '#'+that.$container.attr('id')+' .ms-elem-selectable:not(.ms-selected)',
					selectionSearchString = '#'+that.$container.attr('id')+' .ms-elem-selection.ms-selected';

				    that.qs1 = $selectableSearch.quicksearch(selectableSearchString)
				    .on('keydown', function(e){
				      if (e.which === 40){
					that.$selectableUl.focus();
					return false;
				      }
				    });

				    that.qs2 = $selectionSearch.quicksearch(selectionSearchString)
				    .on('keydown', function(e){
				      if (e.which == 40){
					that.$selectionUl.focus();
					return false;
				      }
				    });
				  },
				  afterSelect: function(){
				    this.qs1.cache();
				    this.qs2.cache();
				  },
				  afterDeselect: function(){
				    this.qs1.cache();
				    this.qs2.cache();
				  }
			};

			if(el_id.indexOf('__prefix__') === -1)
		        	el.multiSelect(options);
	       		
			$('body').on('click', '.grp-add-handler', function() {
				var $group_root = $(this).parents('.grp-collapse');			
				var $group_root_id = $group_root.attr('id');

				setTimeout(function () {
					var $last_added = $group_root.find('.grp-dynamic-form.grp-tbody').last();
					var $select_el = $last_added.find('[multiple=multiple]');
		 			$select_el.multiSelect(options);			
				}, 10);			

			});
		
                })(grp.jQuery || django.jQuery);
        	</script>
        ''' % name
        return mark_safe(output)
