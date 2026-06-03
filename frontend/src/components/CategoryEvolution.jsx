import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const CategoryEvolution = ({ data = [], categories = [] }) => {
  if (!data.length) return <div className="card p-4">No evolution data available</div>;

  return (
    <div className="card p-4 col-span-2">
      <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Category Evolution (Month over Month)</h3>
      <div className="overflow-x-auto">
        <LineChart width={800} height={400} data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
          <XAxis dataKey="month" stroke="#9ca3af" />
          <YAxis stroke="#9ca3af" />
          <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none' }} formatter={(val) => `${val} TND`} />
          <Legend />
          {categories.map((cat, idx) => (
            <Line key={cat} type="monotone" dataKey={cat} stroke={`hsl(${idx * 40}, 70%, 50%)`} />
          ))}
        </LineChart>
      </div>
    </div>
  );
};

export default CategoryEvolution;