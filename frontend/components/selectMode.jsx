import Link from 'next/link';

export default function SelectMode({modalite, activeMod, setActiveMod}) {

    
    return (
		<div >
			<select
				value={activeMod}
				onChange={(e) => setActiveMod(e.target.value)}
			>
				<option value=''>---</option>
				{modalite.map((mod) => (
					<option key={mod.id} value={mod.name}>
						{mod.name}
					</option>
				))}
			</select>

            <div>
            <Link href={`/mode/${activeMod}`}>
                <button disabled={!activeMod}>Go to mode</button>
            </Link>
            {!activeMod && <p>Please select a mode</p>}
            </div>

		</div>
    )}