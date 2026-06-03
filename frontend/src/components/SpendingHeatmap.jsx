import CalendarHeatmap from 'react-calendar-heatmap';
import 'react-calendar-heatmap/dist/styles.css';

const SpendingHeatmap = ({ data }) => {
  const today = new Date();
  const startDate = new Date();
  startDate.setDate(today.getDate() - 90);

  const formattedData = data.map(d => ({ date: d.date, count: d.value }));

  return (
    <div className="overflow-x-auto">
      <CalendarHeatmap
        startDate={startDate}
        endDate={today}
        values={formattedData}
        classForValue={(value) => {
          if (!value || value.count === 0) return 'color-empty';
          if (value.count < 50) return 'color-low';
          if (value.count < 200) return 'color-medium';
          return 'color-high';
        }}
        titleForValue={(value) => value ? `${value.date}: ${value.count} TND` : 'No data'}
      />
      <style>{`
        .color-empty { fill: #e5e7eb; }
        .color-low { fill: #93c5fd; }
        .color-medium { fill: #3b82f6; }
        .color-high { fill: #1e3a8a; }
        .dark .color-empty { fill: #374151; }
        .dark .color-low { fill: #2563eb; }
        .dark .color-medium { fill: #1d4ed8; }
        .dark .color-high { fill: #1e3a8a; }
      `}</style>
    </div>
  );
};

export default SpendingHeatmap;