
import { Html, Head, Main, NextScript } from 'next/document'

export default function Document(): JSX.Element {
    return (
        <Html>
            <Head />
            <body className='text-bg-secondary p-0 m-0'>
                <Main />
                <NextScript />
            </body>
        </Html>
    )
}
