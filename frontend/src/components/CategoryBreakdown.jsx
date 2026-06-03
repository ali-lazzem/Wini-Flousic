import { PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#A569BD', '#F1948A', '#7FB3D5', '#F7DC6F'];

const CategoryBreakdown = ({ data = [] }) => {
  if (!data.length) return <div className="card p-4">No category data available</div>;
  
  return (
    <div className="card p-4">
      <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Spending by Category</h3>
      <div className="flex flex-col md:flex-row items-center justify-center gap-6">
        <PieChart width={400} height={400}>
          <Pie
            data={data}
            dataKey="total"
            nameKey="category"
            cx="50%"
            cy="50%"
            outerRadius={120}
            label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
          >
            {data.map((entry, idx) => (
              <Cell key={`cell-${idx}`} fill={COLORS[idx % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip formatter={(val) => `${val} TND`} contentStyle={{ backgroundColor: '#1f2937', border: 'none' }} />
          <Legend />
        </PieChart>
        <div className="space-y-2">
          {data.map((cat, i) => (
            <div key={cat.category} className="flex justify-between gap-6 text-sm">
              <span className="font-medium text-gray-700 dark:text-gray-300">{cat.category}</span>
              <span className="text-gray-900 dark:text-white">{cat.total} TND ({cat.percentage}%)</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CategoryBreakdown;