import React from 'react';

const ExportCSV = ({ data, fileName }) => {
  const downloadCSV = () => {
    if (!data || data.length === 0) return;

    const headers = Object.keys(data[0]);
    const csvRows = [
      headers.join(','), // Cabeçalhos
      ...data.map(row => headers.map(field => JSON.stringify(row[field], replacer)).join(',')) // Dados
    ];

    const csvContent = csvRows.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });

    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.setAttribute('download', `${fileName}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const replacer = (key, value) => (value === null ? '' : value); // Substitui valores nulos por string vazia

  return (
    <button onClick={downloadCSV} style={{ marginBottom: 20 }}>
      Exportar CSV
    </button>
  );
};

export default ExportCSV;
