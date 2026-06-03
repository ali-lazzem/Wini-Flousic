const Heatmap = ({ data = [] }) => {
  const weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  
  const maxAmount = Math.max(...data.map(d => d.amount || 0), 1);
  
  const getIntensity = (amount) => {
    return Math.min((amount / maxAmount) * 100, 100);
  };
  
  return (
    <div className="card p-4 overflow-x-auto">
      <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Spending Intensity (Weekday vs Month)</h3>
      <table className="min-w-full text-sm">
        <thead>
          <tr>
            <th className="text-gray-600 dark:text-gray-400"></th>
            {months.map(m => <th key={m} className="text-gray-600 dark:text-gray-400">{m}</th>)}
          </tr>
        </thead>
        <tbody>
          {weekdays.map(day => (
            <tr key={day}>
              <td className="font-medium text-gray-700 dark:text-gray-300">{day}</td>
              {months.map(month => {
                const entry = data.find(d => d.weekday === day && d.month === month);
                const amount = entry?.amount || 0;
                const intensity = getIntensity(amount);
                return (
                  <td key={month} className="text-center p-2" style={{ backgroundColor: `rgba(59,130,246,${intensity/100})` }}>
                    <span className="text-gray-900 dark:text-white text-xs">{amount > 0 ? `${amount} TND` : '-'}</span>
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Heatmap;