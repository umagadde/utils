package com.device.quickstart;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.util.*;


@RestController

public class LoanServiceController {
    @Autowired
    ImpactService is;

    @GetMapping("/ping")
    public List<ImpactedScenariosMap> test() throws IOException {
        HashMap<String, List<String>>hs=new HashMap<>();
        List<String >met=new ArrayList<>();
        met.add("method11");
        met.add("method12");
        hs.put("class1",met);
        List<String >met1=new ArrayList<>();
        met1.add("method31");
        hs.put("class3",met1);
        System.out.print(hs);
        return is.fetchGit(hs);


    }

}

