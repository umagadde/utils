package com.device.quickstart;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class ImpactService {
    @Autowired
    ImpactRepository ir;
     public List<ImpactedScenariosMap>fetchGit(HashMap<String,List<String>>hm) throws IOException {
         List<ImpactedScenariosMap>data=ir.findAll();
         List<ImpactedScenariosMap>res=new ArrayList<>();
         for(Map.Entry<String,List<String>>entry:hm.entrySet()){
             List<ImpactedScenariosMap> cl=data.stream().filter(dataObj->dataObj.getClassName().equals(entry.getKey())).collect(Collectors.toList());
             if(cl.size()!=0){
                 for(String met: entry.getValue()){
                 List<Method> ml=cl.get(0).getMethods().stream().filter(metObj->metObj.getMethodName().equals(met)).collect(Collectors.toList());
                 if(ml.size()!=0){
                      List<ImpactedScenariosMap>dsub=res.stream().filter(dataObj->dataObj.getClassName().equals(entry.getKey())).collect(Collectors.toList());
                      if(dsub.size()==0){
                          List<Method>mld=new ArrayList<>();
                          Method m1=new Method(met,ml.get(0).getScenarios());
                          mld.add(m1);
                          res.add(new ImpactedScenariosMap(entry.getKey(),mld));

                      }
                      else{
                          List<Method> msub=dsub.get(0).getMethods().stream().filter(metObj->metObj.getMethodName().equals(met)).collect(Collectors.toList());
                          if(msub.size()==0){
                              Method m1=new Method(met,ml.get(0).getScenarios());
                              List<Method>lm=dsub.get(0).getMethods();
                              lm.add(m1);
                              dsub.get(0).setMethods(lm);
                          }


                      }
                 }

                 }

             }
         }
         return res;
     }

}
