import PageTemplate from "../components/pagetemplate"
import SectionTitleLeftColumm, { SectionTitleRightColumm } from "../components/sectiontitle"
import SectionTextBoxLeftColumm, { SectionTextBoxRightColumm } from "../components/sectiontextbox"
import SectionLink from "../components/sectionlink"

export default function Page() {
    return (
        <PageTemplate pagetitle="Goh Yeow Chong">
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
                    Squatting on <SectionLink href="https://bsky.app/profile/gohyc1993.bsky.social">BlueSky</SectionLink>
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
        </PageTemplate>
    )
}