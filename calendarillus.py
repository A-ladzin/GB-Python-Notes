from tkinter import *
from datetime import timedelta
from tkcalendar import Calendar
 
 
# Апгрейдил календарь, добавил возмодность выбора периода
class Calendarillus(Calendar):
    _sel_date_ = None
    def __init__(self,master,year,month,day,**kw):
        self.root = master
        self.frame = Tk()
        Calendar.__init__(self,master=self.frame,showothermonthdays=False, **kw)
        self._remove_selection()
        self._sel_date = self.root.mindate
        self._sel_date_ = self.root.maxdate
        self._display_selection()
        self.resetButton = Button(self.frame,text = "cancel", command=self.reset)
        self.resetButton.pack(side="bottom",fill = "x")
        
    def reset(self):
        self.root.mindate = None
        self.root.maxdate = None
        self._sel_date = None
        self._sel_date_ = None
        self._remove_selection()
        # --- bindings
    def _on_click(self, event):
        """Select the day on which the user clicked."""
        if self._properties['state'] == 'normal':
            label = event.widget
            if "disabled" not in label.state():
                day = label.cget("text")
                style = label.cget("style")
                if style in ['normal_om.%s.TLabel' % self._style_prefixe, 'we_om.%s.TLabel' % self._style_prefixe]:
                    if label in self._calendar[0]:
                        self._prev_month()
                    else:
                        self._next_month()
                if day:
                    day = int(day)
                    year, month = self._date.year, self._date.month
                    self._remove_selection()
                    if self._sel_date is None:
                        self._sel_date = self.date(year, month, day)
                        self._sel_date_ = self._sel_date
                    elif self._sel_date == self.date(year, month, day):
                        self._sel_date = self._sel_date_
                    elif self._sel_date_ == self.date(year, month, day):
                        self._sel_date_ = self._sel_date
                    elif self._sel_date < self.date(year, month, day):
                        self._sel_date_ = self.date(year, month, day)
                    else:
                        self._sel_date = self.date(year, month, day)
                    self._display_selection()
                    if self._textvariable is not None:
                        self._textvariable.set(self.format_date(self._sel_date))
                    self.event_generate("<<CalendarSelected>>")
                    self.root.mindate = self._sel_date
                    self.root.maxdate = self._sel_date_
            else:
                print("Disable")

                    
    def _display_selection(self):
        w_begin = None
        w_end = None
        d_begin = None
        d_end = None
        m_begin = None
        m_end = None
        """Highlight selected day."""
        if self._sel_date is not None:
            w, d = self._get_day_coords(self._sel_date)
            m_begin = self._sel_date.month
            w_begin = w
            d_begin = d
            if w is not None:
                label = self._calendar[w][d]
                if label.cget('text'):
                    label.configure(style='sel.%s.TLabel' % self._style_prefixe)
        if self._sel_date_ is not None:

            w, d = self._get_day_coords(self._sel_date_)
            w_end = w
            d_end = d
            m_end = self._sel_date_.month
            if w is not None:
                label = self._calendar[w][d]
                if label.cget('text'):
                    label.configure(style='sel.%s.TLabel' % self._style_prefixe)
        if m_begin is not None and m_end is not None:
            if d_begin is None and d_end is not None:
                w_begin = 0
                d_begin = 0
            if d_end is None and d_begin is not None:
                w_end = 5
                d_end = 6
            if w_begin is None and w_end is None:
                if self._sel_date < self._date and self._sel_date_ > self._date:
                    w_begin = 0
                    d_begin = 0
                    w_end = 5
                    d_end = 6
            if w_begin is None or w_end is None:
                return    
            for w in range(w_begin, w_end+1):
                if w == w_begin and w == w_end:
                    for d in range(d_begin+1, d_end):
                        label = self._calendar[w][d]
                        if label.cget('text'):
                            label.configure(style='main.%s.TLabel' % self._style_prefixe)
                elif w == w_begin:
                    for d in range(d_begin+1, 7):
                        label = self._calendar[w][d]
                        if label.cget('text'):
                            label.configure(style='main.%s.TLabel' % self._style_prefixe)

                    
                elif w == w_end:
                    for d in range(0, d_end):
                        label = self._calendar[w][d]
                        if label.cget('text'):
                            label.configure(style='main.%s.TLabel' % self._style_prefixe)
                else:
                    for d in range(0, 7):
                        label = self._calendar[w][d]
                        if label.cget('text'):
                            label.configure(style='main.%s.TLabel' % self._style_prefixe)
                    
                    
                
        
        
                    
                    
    def _remove_selection(self):
        """Remove highlights."""
        for w in range(6):
            for d in range(7):
                if w is not None:
                    week_end = [0, 6] if self['firstweekday'] == 'sunday' else [5, 6]
                    if d in week_end:
                        self._calendar[w][d].configure(style='we.%s.TLabel' % self._style_prefixe)
                    else:
                        self._calendar[w][d].configure(style='normal.%s.TLabel' % self._style_prefixe)
                
                            
    def _show_event(self, date):
        """Display events on date if visible."""
        w, d = self._get_day_coords(date)
        if w is not None:
            label = self._calendar[w][d]
            if not label.cget('text'):
                # this is an other month's day and showothermonth is False
                return
            ev_ids = self._calevent_dates[date]
            i = len(ev_ids) - 1
            while i >= 0 and not self.calevents[ev_ids[i]]['tags']:
                i -= 1
            if i >= 0:
                tag = self.calevents[ev_ids[i]]['tags'][-1]
                label.configure(style='tag_%s.%s.TLabel' % (tag, self._style_prefixe))
            text = '\n'.join(['➢ {}'.format(self.calevents[ev]['text']) for ev in ev_ids])
            self.tooltip_wrapper.remove_tooltip(label)
            self.tooltip_wrapper.add_tooltip(label, text)
            