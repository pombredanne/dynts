from djpcms import views, forms, html
from djpcms.utils import gen_unique_id

from ccy import dateFromString


class EcoForm(forms.Form):
    height = forms.IntegerField()
    service_url = forms.CharField(required = False)
    

class TimeSeriesView(views.ModelView):
    '''``djpcms`` application view for retrieving time-series data as object.
It renders as an econometric plot jQuery plugin and it has an AJAX get response
for fetching data.'''
    isplugin = True
    plugin_form = EcoForm
    description = 'Timeseries and Scatter Plots'
    flot_media = html.Media(js = ['dynts/flot/excanvas.min.js',
                                  'dynts/flot/jquery.flot.js',
                                  'dynts/flot/jquery.flot.selection.js',
                                  'dynts/jquery.flot.text.js',
                                  'dynts/ecoplot/ecoplot.js',
                                  'dynts/decorator.js'])
    _methods = ('get',)
    
    def get_widget(self, djp):
        kwargs = djp.kwargs
        height = max(int(kwargs.get('height',400)),30)
        service_url = kwargs.get('service_url',self.path)
        start = kwargs.get('start',None)
        code = self.get_code_object(djp)
        id = gen_unique_id()
        widget = html.Widget('div', id = id, cn = 'econometric-plot')\
                .addData('height',height)\
                .addData('start',start)\
                .addData('url',service_url)
        if code:
            widget.addData('commandline',{'show':False,'symbol':code})
        return widget
            
    def render(self, djp):
        return self.get_widget(djp).render(djp)
    
    def get_code_object(self, djp):
        return self.appmodel.get_code_object(djp)
    
    def ajax_get_response(self, djp):
        request = djp.request
        return self.econometric_data(request, dict(request.GET.items()))
           
    def econometric_data(self, request, data):
        #Obtain the data
        cts    = data.get('command',None)
        start  = data.get('start',None)
        end    = data.get('end',None)
        period = data.get('period',None)
        #object = self.get_object(cts)
        #if object:
        #    cts = self.codeobject(object)
        if start:
            start = dateFromString(str(start))
        if end:
            end = dateFromString(str(end))
        return self.appmodel.getdata(request,cts,start,end)
    
    def media(self):
        return self.flot_media
    
