import Header from "../components/header";
import Footer from "../components/footer";
import Image from "next/image";
import SelectMode from "../components/selectMode";
import Presentation from "../components/presentation";
import { useState } from 'react';
import modalite from '../data/modality.json';



export default function Home() {

  const [activeMod, setActiveMod] = useState('')
  return (
    <div >
      <Header>
        <h1>Car Brand Explanations</h1>
        <h2>Test Project</h2>
      </Header>
      

      <Presentation  />
      <SelectMode modalite = {modalite} activeMod={activeMod} setActiveMod={setActiveMod} />


      <Footer />
    </div>
  );
}