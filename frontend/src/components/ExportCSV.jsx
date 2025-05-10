import React from 'react';

export default function ExportCSV({ data, fileName, disabled }) {
  // Replacer para valores nulos
  const replacer = (key, value) => (value === null ? '' : value);

  const downloadCSV = () => {
    if (!data || data.length === 0) return;

    const headers = Object.keys(data[0]);
    const csvRows = [
      headers.join(','), // Cabeçalhos
      ...data.map(row =>
        headers.map(field => JSON.stringify(row[field] ?? '', replacer)).join(',')
      ) // Linhas de dados
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

  return (
    <button onClick={downloadCSV} disabled={disabled} style={{ marginRight: 16 }}>
      Exportar CSV
    </button>
  );
}
