const ExportButton = ({ endpoint, filename = 'export.csv' }) => {
  const handleExport = () => {
    window.open(`${endpoint}?format=csv`, '_blank');
  };
  return (
    <button
      onClick={handleExport}
      className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition"
    >
      Export CSV
    </button>
  );
};

export default ExportButton;