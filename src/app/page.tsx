import PageTitle from "../components/pagetitle"
import SectionTitleLeftColumm, { SectionTitleRightColumm } from "../components/sectiontitle"
import SectionTextBoxLeftColumm, { SectionTextBoxRightColumm } from "../components/sectiontextbox"

export default function Page() {
    return (
        <div className="w-9/10 flex flex-col justify-center">
            <div className="p-2 border-b-2 border-sky-100">
                <PageTitle>
                    Goh Yeow Chong
                </PageTitle>
            </div>
            <div className="flex flex-row flex-wrap justify-center">
                <div className="w-1/2 py-2 px-4 flex flex-col justify-right">
                    <SectionTitleLeftColumm>
                        Stack
                    </SectionTitleLeftColumm>
                    <SectionTextBoxLeftColumm>
                        Next.js (Next Framework + React + TailwindCSS)
                    </SectionTextBoxLeftColumm>
                    <SectionTitleLeftColumm>
                        Contact
                    </SectionTitleLeftColumm>
                    <SectionTextBoxLeftColumm>
                        TBU
                    </SectionTextBoxLeftColumm>
                </div>
                <div className="w-1/2 py-2 px-4 flex flex-col justify-left">
                    <SectionTitleRightColumm>
                        Current
                    </SectionTitleRightColumm>
                    <SectionTextBoxRightColumm>
                        Junior Data Analyst
                    </SectionTextBoxRightColumm>
                    <SectionTitleRightColumm>
                        Aspiring
                    </SectionTitleRightColumm>
                    <SectionTextBoxRightColumm>
                        Data Engineer
                        <br></br>
                        Lecturer
                        <br></br>
                        Sketch + Digital Artist
                    </SectionTextBoxRightColumm>
                </div>
            </div>
        </div>
    )
}