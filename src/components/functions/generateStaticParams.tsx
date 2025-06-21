import { readdir } from "fs/promises"

export default function generateStaticParamsGenerator(path_tag: string, code_location: string) {
    async function generateStaticParams() {
        
        const files = await readdir(code_location, { recursive: true, withFileTypes: true }).then(
            (fileList) => fileList.filter(
                (file) => file.isFile() && /\.mdx?$/i.test(file.name)
            ).map(
                (file) => ({ [path_tag] : file.parentPath.concat("/", file.name).replace(/.mdx?$/i, "").replace(/^\//, "").replace(`${code_location}/`, "").split("/") })
            )
        )

        return files
    }

    return generateStaticParams
}