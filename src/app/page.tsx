import PageTemplate from "../components/page/pagetemplate"
import SectionTitleLeftColumn, { SectionTitleRightColumn } from "../components/section/sectiontitle"
import SectionTextBoxLeftColumn, { SectionTextBoxRightColumn } from "../components/section/sectiontextbox"
import SectionLink from "../components/section/sectionlink"

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
                    Sketch + Digital Artist
                    <br></br>
                    Lecturer
                </SectionTextBoxRightColumn>
            </div>
        </PageTemplate>
    )
}