import Image from 'next/image'

export default function Home() {
  return (
    <main className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-5xl">Goh Yeow Chong</h1>
      <div className="w-1/3">
        <div className="flex">
          <h2 className="text-lg text-right w-1/3 mr-4">Current</h2>
          <div className="flex flex-col w-2/3">
            <h2 className="text-lg">Research Assistant</h2>
            <p className="text-xs">Center for Research in Child Development<br/>National Institute of Education<br/>Nanyang Technological University</p>
          </div>
        </div>
        <div className="flex">
          <p className="text-lg text-right w-1/3 mr-4">Role</p>
          <div className="flex flex-col w-2/3">
            <h2 className="text-lg">Data-Related</h2>
            <p className="text-xs">Data cleaning<br/>Feature engineering<br/>Data merging<br/>Longitudinal data analysis</p>
            <h2 className="text-lg">Other</h2>
            <p className="text-xs">Literature reviews</p>
          </div>
        </div>
        <div className="flex">
          <p className="text-lg text-right w-1/3 mr-4">Aspiring</p>
          <div className="flex flex-col w-2/3">
            <h2 className="text-lg">Data Analyst</h2>
          </div>
        </div>
        <div className="flex">
          <p className="text-lg text-right w-1/3 mr-4">Languages</p>
          <div className="flex flex-col w-2/3">
            <h2 className="text-lg">Main</h2>
            <p className="text-xs">Python</p>
            <h2 className="text-lg">Other</h2>
            <p className="text-xs">R<br/>Julia<br/>SQL<br/><a className="hover:text-slate-500" href="https://www.freecodecamp.org/certification/yc-goh/foundational-c-sharp-with-microsoft">C#</a> (currently learning)<br/>JavaScript (currently learning)</p>
          </div>
        </div>
        <div className="flex">
          <p className="text-lg text-right w-1/3 mr-4">Contact</p>
          <div className="flex flex-col w-2/3">
            <a className="text-lg hover:text-slate-500" href="mailto:gohyc1993@gmail.com">Email</a>
            <a className="text-lg">LinkedIn (TBU)</a>
          </div>
        </div>
      </div>
    </main>
  )
}
