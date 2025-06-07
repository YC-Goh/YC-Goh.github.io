import { readdir } from "fs/promises"

export default function generateStaticParamsGenerator(code_location: string) {
    async function generateStaticParams() {
        
        const files = await readdir(code_location, { recursive: true, withFileTypes: true }).then(
            (fileList) => fileList.filter(
                (file) => file.isFile()
            ).filter(
                (file) => /\.mdx?$/i.test(file.name)
            ).map(
                (file) => ({ fymd : file.parentPath.concat("/", file.name).replace(/.mdx?$/i, "").replace(/^\//, "").replace(`${code_location}/`, "").split("/") })
            )
        )

        console.log(files)

        return files
    }

    return generateStaticParams
}
