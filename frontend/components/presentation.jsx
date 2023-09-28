import Link from 'next/link';
export default function Presentation({props}) {

  return (
    <div style={{ display: "flex", justifyContent: "center" }}>
        <div>
            <p>Upload media</p>
        </div>
        <div>
            <p>Analyzing</p>
        </div>
        <div>
            <p>Explanations</p>
        </div>
    </div>
  );
}