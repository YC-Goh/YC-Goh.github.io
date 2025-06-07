import { readdir } from "fs/promises"
import SectionLink from "../section/sectionlink"
import React from "react"
import SectionUnsortedList from "../section/sectionunsortedlist"
import { SectionTextBoxRightColumn } from "../section/sectiontextbox"

function createTree(file_paths: Array<string>, section_root: string) {

    const file_tree = file_paths.map(
        (file) => file.split("/")
    )

    function _createTreeLevel(file_paths: Array<Array<string>>, parent_path: Array<string>) {

        const file_list = file_paths.filter(
            (file) => file.length === 1
        ).map(
            (file) => file[0]
        )

        const folder_list = file_paths.filter(
            (file) => file.length > 1
        ).map(
            (file) => file[0]
        )

        const level_list = file_paths.map(
            (file) => file[0]
        ).filter(
            (elem, i, arr) => i === arr.indexOf(elem)
        ).map(
            (file) => {
                const file_path = [...parent_path, file]

                let list_item: React.ReactNode
                if (file_list.includes(file)) {
                    list_item = <SectionLink href={["", ...parent_path, file].join("/")}>{ file }</SectionLink>
                } else {
                    list_item = <SectionTextBoxRightColumn>{ file }</SectionTextBoxRightColumn>
                }

                let sub_list: React.ReactNode
                if (folder_list.includes(file)) {
                    const sub_file_paths = file_paths.filter(
                        (sub_file) => sub_file.length > 1 && sub_file[0] == file
                    ).map(
                        (sub_file) => sub_file.slice(1)
                    )
                    sub_list = _createTreeLevel(sub_file_paths, file_path)
                    return (
                        <li key={ file_path.join("-") }>
                            { list_item }
                            { sub_list }
                        </li>
                    )
                } else {
                    return (<li key={ file_path.join("-") }>{ list_item }</li>)
                }
            }
        )

        return (<SectionUnsortedList>{ level_list }</SectionUnsortedList>)

    }

    return _createTreeLevel(file_tree, section_root.split("/"))
}

export default function generateFileTreeGenerator(code_root: string, section_path: string) {
    async function generateFileTree() {

        //  Generating the treefile needs to be recursive.
        //  1:  Loop over all files and folders on the first level.
        //  2a: For each folder, if a file of the same name does not exist, add a text entry to the list.
        //  2b: Then, for each folder, recurse this function and add the returns below the text or link entry.
        //  3:  For each file, if a folder of the same name does not exist, add a link to the list.

        const code_location = [code_root, section_path].join("/")

        const files = await readdir(code_location, { recursive: true, withFileTypes: true }).then(
            (fileList) => fileList.filter(
                (file) => file.isFile() && /\.mdx?$/i.test(file.name)
            ).map(
                (file) => file.parentPath.concat("/", file.name.replace(/\.mdx?$/i, "")).replace(`${code_location}/`, "")
            )
        )

        const file_tree = createTree(files, section_path)

        return file_tree
    }

    return generateFileTree
}