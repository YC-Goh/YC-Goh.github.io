
// import { useRouter } from "next/router";
import { GetStaticProps } from "next";
import { GetStaticPaths } from "next";
// import { ParsedUrlQuery } from "querystring";
// import { AppProps } from "next/app";
import PageTemplate from '../../components/page-template';
import Content from '../../components/content';
import fs from 'fs/promises';
import path from 'path';
import 'katex/dist/katex.css';

let thisPublicPath = ['public', 'data-projects']

export default function NoteBook (props: {nbContent: string}) {
    return (PageTemplate(Content(props.nbContent, 'markdown')));
};

export let getStaticProps: GetStaticProps<{nbContent:string}> = async (context) => {
    let nbContent = await fs.readFile(path.resolve(...thisPublicPath, `${context.params!.nbid}.md`), {'encoding': 'utf8'})
    return {
        props: {
            nbContent
        }
    };
};

export let getStaticPaths: GetStaticPaths = async () => {
    let files = await fs.readdir(path.resolve(...thisPublicPath));
    files = files.filter(function (file) {
        return /.md$/i.test(file);
    });
    let filePaths = files.map(function (file) {
        return { params: { nbid: file.replace(/.md$/i, '') } }
    });
    return {
        paths: filePaths,
        fallback: false
    };
};
