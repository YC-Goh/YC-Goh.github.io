import Image from 'next/image'

export default function Home() {
  return (
    <main className="flex flex-col mx-auto">
      <div className="flex flex-row justify-center">
        <h1 className="text-5xl">Goh Yeow Chong</h1>
      </div>
      <div>
        <div className="flex flex-row">
          <h2 className="text-lg text-right w-1/2 mr-4">Current</h2>
          <div className="flex flex-col w-1/2">
            <h2 className="text-lg">Research Assistant</h2>
            <p className="text-xs">Center for Research in Child Development<br/>National Institute of Education<br/>Nanyang Technological University</p>
          </div>
        </div>
        <div className="flex">
          <p className="text-lg text-right w-1/2 mr-4">Role</p>
          <div className="flex flex-col w-1/2">
            <h2 className="text-lg">Data Work</h2>
            <p className="text-xs">
              Data cleaning<br/>
              Feature engineering<br/>
              Exploratory data analysis<br/>
              Classical statistical inference<br/>
              Longitudinal data analysis<br/>
              Visualisation
            </p>
            <h2 className="text-lg">Other</h2>
            <p className="text-xs">Literature reviews</p>
            <p className="text-xs">Data documentation</p>
          </div>
        </div>
        <div className="flex">
          <p className="text-lg text-right w-1/2 mr-4">Aspiring</p>
          <div className="flex flex-col w-1/2">
            <h2 className="text-lg">Data Analyst</h2>
          </div>
        </div>
        <div className="flex">
          <p className="text-lg text-right w-1/2 mr-4">Languages</p>
          <div className="flex flex-col w-1/2">
            <h2 className="text-lg">Main</h2>
            <p className="text-xs">Python</p>
            <h2 className="text-lg">Other (Data-Related)</h2>
            <p className="text-xs">
              R<br/>
              Julia<br/>
              SQL
            </p>
            <h2 className="text-lg">Other (Statistical Program Syntax)</h2>
            <p className="text-xs">
              STATA<br/>
              SPSS<br/>
              MPlus
            </p>
            <h2 className="text-lg">Other (Personal Use)</h2>
            <p className="text-xs">
              <a className="hover:text-slate-500" href="https://www.freecodecamp.org/certification/yc-goh/foundational-c-sharp-with-microsoft">C#</a><br/>
              <a className="hover:text-slate-500" href="https://www.freecodecamp.org/certification/yc-goh/front-end-development-libraries">JavaScript</a>
            </p>
          </div>
        </div>
        <div className="flex mt-1">
          <p className="text-lg text-right w-1/2 mr-4">Current Learning Journey</p>
          <div className="flex flex-col w-1/2">
            <h2 className="text-lg">Data</h2>
            <p className="text-xs">
              Analysing <a className="hover:text-slate-500" href="https://www.worldvaluessurvey.org/">WVS</a> Data<br/>
            </p>
            <h2 className="text-lg">Other</h2>
            <p className="text-xs">
              Personal Blog (<a className="hover:text-slate-500" href="https://nextjs.org/docs/pages/building-your-application/configuring/mdx">Next Step</a>)<br/>
              Applying C# (<a className="hover:text-slate-500" href="https://docs.godotengine.org/en/stable/getting_started/step_by_step/scripting_languages.html#net-c">Next Step</a>)
            </p>
          </div>
        </div>
      </div>
    </main>
  )
}
