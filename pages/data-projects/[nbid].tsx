
// import { useRouter } from "next/router";
import { GetStaticProps } from "next";
import { GetStaticPaths } from "next";
// import { ParsedUrlQuery } from "querystring";
// import { AppProps } from "next/app";
import PageTemplate from '../../components/page-template';
import Content from '../../components/content';
import fs from 'fs/promises';
import path from 'path';

export default function NoteBook (props: {nbContent: string}) {
    return (PageTemplate(Content(props.nbContent)));
};

export let getStaticProps: GetStaticProps<{nbContent:string}> = async (context) => {
    let nbContent = await fs.readFile(path.resolve('pages', 'data-projects', `${context.params!.nbid}.md`), {'encoding': 'utf8'})
    return {
        props: {
            nbContent
        }
    };
};

export let getStaticPaths: GetStaticPaths = async () => {
    return {
        paths: [{ params: {nbid: 'sg-marriages-pam'} }],
        fallback: false
    };
};
