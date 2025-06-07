import PageTemplate from "../components/pagetemplate"
import SectionTitleLeftColumn, { SectionTitleRightColumn } from "../components/sectiontitle"
import SectionTextBoxLeftColumn, { SectionTextBoxRightColumn } from "../components/sectiontextbox"
import SectionLink from "../components/sectionlink"

export default function Page() {
    return (
        <PageTemplate pagetitle="Goh Yeow Chong">
            <div className="w-1/2 py-2 px-4 flex flex-col justify-right">
                <SectionTitleLeftColumn>
                    Stack
                </SectionTitleLeftColumn>
                <SectionTextBoxLeftColumn>
                    Next.js (Next Framework + React + TailwindCSS)
                </SectionTextBoxLeftColumn>
                <SectionTitleLeftColumn>
                    Contact
                </SectionTitleLeftColumn>
                <SectionTextBoxLeftColumn>
                    Squatting on <SectionLink href="https://bsky.app/profile/gohyc1993.bsky.social">BlueSky</SectionLink>
                </SectionTextBoxLeftColumn>
            </div>
            <div className="w-1/2 py-2 px-4 flex flex-col justify-left">
                <SectionTitleRightColumn>
                    Current
                </SectionTitleRightColumn>
                <SectionTextBoxRightColumn>
                    Junior Data Analyst
                </SectionTextBoxRightColumn>
                <SectionTitleRightColumn>
                    Aspiring
                </SectionTitleRightColumn>
                <SectionTextBoxRightColumn>
                    Data Engineer
                    <br></br>
                    Lecturer
                    <br></br>
                    Sketch + Digital Artist
                </SectionTextBoxRightColumn>
            </div>
        </PageTemplate>
    )
}