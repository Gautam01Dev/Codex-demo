import { Line } from 'react-chartjs-2'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend } from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend)

export default function PredictionChart({ latest, shortTerm, midTerm }) {
  const data = {
    labels: ['Today', '7 Days', '90 Days'],
    datasets: [
      {
        label: 'Price Projection',
        data: [latest, shortTerm, midTerm],
        borderColor: '#5b9dff',
        backgroundColor: 'rgba(91,157,255,0.25)',
        tension: 0.25,
      },
    ],
  }

  return <Line data={data} />
}
